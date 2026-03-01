from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import BINARY_SENSOR_DESCRIPTIONS, DOMAIN
from .entity import ClockForgeEntity


def _read_path(data: dict, path: tuple[str, ...]):
    value = data
    for key in path:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


class ClockForgeBinarySensor(ClockForgeEntity, BinarySensorEntity):
    def __init__(self, coordinator, entry, key: str, name: str, path: tuple[str, ...], device_class: str | None) -> None:
        super().__init__(coordinator, entry, key, name)
        self._path = path
        self._attr_device_class = device_class

    @property
    def is_on(self) -> bool:
        return bool(_read_path(self.coordinator.data, self._path))


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    entities = [
        ClockForgeBinarySensor(coordinator, entry, key, name, path, device_class)
        for key, name, path, device_class in BINARY_SENSOR_DESCRIPTIONS
    ]
    async_add_entities(entities)
