from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, SENSOR_DESCRIPTIONS
from .entity import ClockForgeEntity

UNIT_MAP = {
    "°C": "°C",
    "hPa": "hPa",
    "lx": "lx",
    "%": "%",
    "B": "B",
    "MHz": "MHz",
    "dBm": "dBm",
    "s": "s",
}


def _read_path(data: dict, path: tuple[str, ...]):
    value = data
    for key in path:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


class ClockForgeSensor(ClockForgeEntity, SensorEntity):
    def __init__(self, coordinator, entry, key: str, name: str, path: tuple[str, ...], device_class: str | None, unit: str | None) -> None:
        super().__init__(coordinator, entry, key, name)
        self._path = path
        self._attr_device_class = device_class
        self._attr_native_unit_of_measurement = UNIT_MAP.get(unit, unit)

    @property
    def native_value(self):
        value = _read_path(self.coordinator.data, self._path)
        if self._key == "chip_temperature" and not self.coordinator.data.get("system", {}).get("chipTemperatureValid"):
            return None
        return value


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    entities = [
        ClockForgeSensor(coordinator, entry, key, name, path, device_class, unit)
        for key, name, path, device_class, unit in SENSOR_DESCRIPTIONS
    ]
    async_add_entities(entities)
