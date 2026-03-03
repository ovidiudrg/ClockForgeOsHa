from __future__ import annotations

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, NUMBER_DESCRIPTIONS
from .entity import ClockForgeEntity


def _read_path(data: dict, path: tuple[str, ...]):
    value = data
    for key in path:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


class ClockForgeNumber(ClockForgeEntity, NumberEntity):
    def __init__(
        self,
        coordinator,
        entry,
        key: str,
        name: str,
        path: tuple[str, ...],
        min_value: float,
        max_value: float,
        step: float,
        unit: str | None,
        settings_key: str,
        scale: float,
    ) -> None:
        super().__init__(coordinator, entry, key, name)
        self._path = path
        self._settings_key = settings_key
        self._scale = scale
        self._attr_native_min_value = min_value
        self._attr_native_max_value = max_value
        self._attr_native_step = step
        self._attr_native_unit_of_measurement = unit
        self._attr_mode = "box"

    @property
    def native_value(self) -> float | None:
        value = _read_path(self.coordinator.data, self._path)
        if value is None:
            return None
        return float(value) * self._scale

    async def async_set_native_value(self, value: float) -> None:
        raw_value = round(float(value) / self._scale, 6)
        if float(raw_value).is_integer():
            payload = str(int(raw_value))
        else:
            payload = str(raw_value)
        await self.coordinator.async_save_settings(**{self._settings_key: payload})


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    entities = [
        ClockForgeNumber(coordinator, entry, key, name, path, min_value, max_value, step, unit, settings_key, scale)
        for key, name, path, min_value, max_value, step, unit, settings_key, scale in NUMBER_DESCRIPTIONS
    ]
    async_add_entities(entities)
