from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, SWITCH_DESCRIPTIONS
from .entity import ClockForgeEntity


def _read_path(data: dict, path: tuple[str, ...]):
    value = data
    for key in path:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


class ClockForgeSwitch(ClockForgeEntity, SwitchEntity):
    def __init__(
        self,
        coordinator,
        entry,
        key: str,
        name: str,
        path: tuple[str, ...],
        icon: str | None,
        device_class: str | None,
        settings_key: str,
    ) -> None:
        super().__init__(coordinator, entry, key, name)
        self._path = path
        self._attr_icon = icon
        self._attr_device_class = device_class
        self._settings_key = settings_key

    @property
    def is_on(self) -> bool:
        return bool(_read_path(self.coordinator.data, self._path))

    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.async_save_settings(**{self._settings_key: "true"})

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.async_save_settings(**{self._settings_key: "false"})


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    entities = [
        ClockForgeSwitch(coordinator, entry, key, name, path, icon, device_class, settings_key)
        for key, name, path, icon, device_class, settings_key in SWITCH_DESCRIPTIONS
    ]
    async_add_entities(entities)
