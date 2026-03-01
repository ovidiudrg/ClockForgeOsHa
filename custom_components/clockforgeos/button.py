from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    BUTTON_DISPLAY_TOGGLE,
    BUTTON_SYNC,
    BUTTON_WIFI_CONNECT,
    BUTTON_WIFI_DISCONNECT,
    DOMAIN,
)
from .entity import ClockForgeEntity


class ClockForgeButton(ClockForgeEntity, ButtonEntity):
    def __init__(
        self,
        coordinator,
        entry,
        key: str,
        name: str,
        mqtt_suffix: str,
        http_action: str,
        mqtt_payload: str | int | dict | None = None,
        http_extra: dict | None = None,
    ) -> None:
        super().__init__(coordinator, entry, key, name)
        self._mqtt_suffix = mqtt_suffix
        self._http_action = http_action
        self._mqtt_payload = mqtt_payload
        self._http_extra = http_extra or {}

    async def async_press(self) -> None:
        await self.coordinator.async_execute_command(
            mqtt_suffix=self._mqtt_suffix,
            http_action=self._http_action,
            mqtt_payload=self._mqtt_payload,
            http_extra=self._http_extra,
        )


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    entities = [
        ClockForgeButton(coordinator, entry, BUTTON_SYNC, "Sync Time", "time/sync", "sync"),
        ClockForgeButton(coordinator, entry, BUTTON_DISPLAY_TOGGLE, "Toggle Display", "display/set", "display_toggle", "toggle"),
        ClockForgeButton(coordinator, entry, BUTTON_WIFI_CONNECT, "WiFi Connect", "wifi/connect", "wifi_connect"),
        ClockForgeButton(coordinator, entry, BUTTON_WIFI_DISCONNECT, "WiFi Disconnect", "wifi/disconnect", "wifi_disconnect"),
    ]
    async_add_entities(entities)
