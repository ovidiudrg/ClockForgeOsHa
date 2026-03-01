from __future__ import annotations

import asyncio
import json
from datetime import timedelta
from typing import Any
from uuid import uuid4

from aiohttp import ClientError

from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import ClockForgeApi
from .const import (
    CONF_CONTROL_TRANSPORT,
    CONF_SCAN_INTERVAL,
    CONTROL_TRANSPORT_AUTO,
    CONTROL_TRANSPORT_MQTT,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_CONTROL_TRANSPORT,
    DEFAULT_SCAN_INTERVAL_SECONDS,
    DOMAIN,
)

MQTT_COMMAND_TIMEOUT_SECONDS = 8


class ClockForgeCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, api: ClockForgeApi) -> None:
        self.api = api
        self.entry = entry
        self.last_command_result: dict[str, Any] | None = None
        self._mqtt_unsubscribe = None
        self._mqtt_result_topic: str | None = None
        self._pending_results: dict[str, asyncio.Future[dict[str, Any]]] = {}

        super().__init__(
            hass,
            logger=hass.data[DOMAIN]["logger"],
            name="ClockForgeOS",
            update_interval=DEFAULT_SCAN_INTERVAL,
        )
        self._apply_options()

    def _apply_options(self) -> None:
        interval_seconds = self.entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL_SECONDS)
        self.update_interval = timedelta(seconds=interval_seconds)

    async def async_setup_runtime(self) -> None:
        await self._async_refresh_mqtt_subscription()

    async def async_shutdown_runtime(self) -> None:
        await self._async_unsubscribe_mqtt()
        for future in self._pending_results.values():
            if not future.done():
                future.cancel()
        self._pending_results.clear()

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            data = await self.api.get_status()
        except (ClientError, TimeoutError, ValueError) as err:
            raise UpdateFailed(f"ClockForgeOS status update failed: {err}") from err

        self._apply_options()
        await self._async_refresh_mqtt_subscription(data)
        return data

    def _control_transport(self) -> str:
        return self.entry.options.get(CONF_CONTROL_TRANSPORT, DEFAULT_CONTROL_TRANSPORT)

    def _mqtt_topics(self) -> tuple[str | None, str | None]:
        network = self.data.get("network", {}) if self.data else {}
        return network.get("mqttCommandBase"), network.get("mqttResultTopic")

    def _mqtt_allowed(self) -> bool:
        return self._control_transport() in (CONTROL_TRANSPORT_AUTO, CONTROL_TRANSPORT_MQTT)

    def _mqtt_supports_correlation_ids(self) -> bool:
        network = self.data.get("network", {}) if self.data else {}
        return bool(network.get("mqttCorrelationIds"))

    async def _async_refresh_mqtt_subscription(self, data: dict[str, Any] | None = None) -> None:
        status = data or self.data or {}
        network = status.get("network", {})
        result_topic = network.get("mqttResultTopic")

        if not self._mqtt_allowed() or not result_topic:
            await self._async_unsubscribe_mqtt()
            return

        if self._mqtt_result_topic == result_topic and self._mqtt_unsubscribe is not None:
            return

        await self._async_unsubscribe_mqtt()

        if not await mqtt.async_wait_for_mqtt_client(self.hass):
            return

        @callback
        def _handle_result(message: mqtt.ReceiveMessage) -> None:
            try:
                result = json.loads(message.payload)
            except json.JSONDecodeError:
                result = {
                    "ok": False,
                    "detail": "invalid_json",
                    "payload": message.payload,
                }

            self.last_command_result = result
            request_id = result.get("requestId")
            if request_id and request_id in self._pending_results:
                future = self._pending_results.pop(request_id)
                if not future.done():
                    future.set_result(result)

            self.async_update_listeners()

        self._mqtt_unsubscribe = await mqtt.async_subscribe(self.hass, result_topic, _handle_result, 0)
        self._mqtt_result_topic = result_topic

    async def _async_unsubscribe_mqtt(self) -> None:
        if self._mqtt_unsubscribe is not None:
            self._mqtt_unsubscribe()
            self._mqtt_unsubscribe = None
        self._mqtt_result_topic = None

    async def async_execute_http_command(self, action: str, **extra: Any) -> dict[str, Any]:
        result = await self.api.post_command(action, **extra)
        self.last_command_result = result
        await self.async_request_refresh()
        return result

    async def async_execute_command(
        self,
        *,
        mqtt_suffix: str,
        http_action: str,
        mqtt_payload: str | int | float | bool | dict[str, Any] | None = None,
        http_extra: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        transport = self._control_transport()
        command_base, _ = self._mqtt_topics()
        use_mqtt = transport == CONTROL_TRANSPORT_MQTT or (
            transport == CONTROL_TRANSPORT_AUTO and command_base
        )

        if use_mqtt and command_base:
            if not await mqtt.async_wait_for_mqtt_client(self.hass):
                self.last_command_result = {
                    "ok": False,
                    "detail": "mqtt_client_unavailable",
                    "command": mqtt_suffix,
                }
                self.async_update_listeners()
                return self.last_command_result

            request_id = uuid4().hex
            payload: str
            result_future: asyncio.Future[dict[str, Any]] | None = None

            if self._mqtt_supports_correlation_ids():
                envelope: dict[str, Any] = {"requestId": request_id}
                if mqtt_payload is not None:
                    envelope["value"] = mqtt_payload
                payload = json.dumps(envelope)
                result_future = self.hass.loop.create_future()
                self._pending_results[request_id] = result_future
            else:
                if isinstance(mqtt_payload, dict):
                    payload = json.dumps(mqtt_payload)
                elif mqtt_payload is None:
                    payload = ""
                else:
                    payload = str(mqtt_payload)

            await mqtt.async_publish(self.hass, f"{command_base}/{mqtt_suffix}", payload, 0, False)

            if result_future is not None:
                try:
                    result = await asyncio.wait_for(result_future, timeout=MQTT_COMMAND_TIMEOUT_SECONDS)
                except asyncio.TimeoutError:
                    self._pending_results.pop(request_id, None)
                    result = {
                        "contract": self.data.get("network", {}).get("mqttContractVersion", "unknown") if self.data else "unknown",
                        "requestId": request_id,
                        "command": mqtt_suffix,
                        "ok": False,
                        "detail": "timeout",
                    }
                    self.last_command_result = result
                    self.async_update_listeners()
                else:
                    self.last_command_result = result
                    self.async_update_listeners()
                return result

            self.last_command_result = {
                "contract": self.data.get("network", {}).get("mqttContractVersion", "unknown") if self.data else "unknown",
                "command": mqtt_suffix,
                "ok": True,
                "detail": "published",
            }
            self.async_update_listeners()
            return self.last_command_result

        if transport == CONTROL_TRANSPORT_MQTT and not command_base:
            self.last_command_result = {
                "ok": False,
                "detail": "mqtt_command_base_missing",
                "command": mqtt_suffix,
            }
            self.async_update_listeners()
            return self.last_command_result

        return await self.async_execute_http_command(http_action, **(http_extra or {}))
