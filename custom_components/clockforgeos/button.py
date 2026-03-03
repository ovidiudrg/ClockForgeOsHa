from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    BUTTON_DESCRIPTIONS,
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
        mqtt_suffix: str | None,
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
        if self._mqtt_suffix is None:
            await self.coordinator.async_execute_http_command(self._http_action, **self._http_extra)
            return
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
        ClockForgeButton(coordinator, entry, key, name, mqtt_suffix, http_action, mqtt_payload, http_extra)
        for key, name, mqtt_suffix, http_action, mqtt_payload, http_extra in BUTTON_DESCRIPTIONS
    ]
    async_add_entities(entities)
