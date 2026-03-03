from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, SELECT_DESCRIPTIONS
from .entity import ClockForgeEntity


def _read_path(data: dict, path: tuple[str, ...]):
    value = data
    for key in path:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


class ClockForgeSelect(ClockForgeEntity, SelectEntity):
    def __init__(
        self,
        coordinator,
        entry,
        key: str,
        name: str,
        path: tuple[str, ...],
        value_map: dict[str, str],
        settings_key: str,
    ) -> None:
        super().__init__(coordinator, entry, key, name)
        self._path = path
        self._value_map = value_map
        self._label_to_value = {label: value for value, label in value_map.items()}
        self._settings_key = settings_key
        self._attr_options = list(value_map.values())

    @property
    def current_option(self) -> str | None:
        value = _read_path(self.coordinator.data, self._path)
        if value is None:
            return None
        normalized = str(value).lower() if isinstance(value, bool) else str(value)
        return self._value_map.get(normalized)

    async def async_select_option(self, option: str) -> None:
        value = self._label_to_value.get(option)
        if value is None:
            return
        await self.coordinator.async_save_settings(**{self._settings_key: value})


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    entities = [
        ClockForgeSelect(coordinator, entry, key, name, path, value_map, settings_key)
        for key, name, path, value_map, settings_key in SELECT_DESCRIPTIONS
    ]
    async_add_entities(entities)
