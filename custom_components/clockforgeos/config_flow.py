from __future__ import annotations

from typing import Any

import voluptuous as vol
from aiohttp import ClientError

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import ClockForgeApi
from .const import (
    CONF_CONTROL_TRANSPORT,
    CONF_SCAN_INTERVAL,
    CONTROL_TRANSPORT_AUTO,
    CONTROL_TRANSPORT_HTTP,
    CONTROL_TRANSPORT_MQTT,
    DEFAULT_CONTROL_TRANSPORT,
    DEFAULT_SCAN_INTERVAL_SECONDS,
    DOMAIN,
)


def _options_schema(options: dict[str, Any]) -> vol.Schema:
    return vol.Schema(
        {
            vol.Required(
                CONF_CONTROL_TRANSPORT,
                default=options.get(CONF_CONTROL_TRANSPORT, DEFAULT_CONTROL_TRANSPORT),
            ): vol.In([CONTROL_TRANSPORT_AUTO, CONTROL_TRANSPORT_HTTP, CONTROL_TRANSPORT_MQTT]),
            vol.Required(
                CONF_SCAN_INTERVAL,
                default=options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL_SECONDS),
            ): vol.All(vol.Coerce(int), vol.Range(min=5, max=300)),
        }
    )


class ClockForgeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                session = async_get_clientsession(self.hass)
                api = ClockForgeApi(
                    user_input[CONF_HOST],
                    user_input.get(CONF_USERNAME),
                    user_input.get(CONF_PASSWORD),
                    session,
                )
                status = await api.get_status()
            except (ClientError, TimeoutError, ValueError):
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(status.get("profile", user_input[CONF_HOST]))
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=f"ClockForgeOS {status.get('profile', user_input[CONF_HOST])}",
                    data=user_input,
                    options={
                        CONF_CONTROL_TRANSPORT: DEFAULT_CONTROL_TRANSPORT,
                        CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL_SECONDS,
                    },
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_HOST): str,
                vol.Optional(CONF_USERNAME): str,
                vol.Optional(CONF_PASSWORD): str,
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    @staticmethod
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> ClockForgeOptionsFlow:
        return ClockForgeOptionsFlow(config_entry)


class ClockForgeOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self._config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=_options_schema(self._config_entry.options),
        )
