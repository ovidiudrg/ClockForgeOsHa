from __future__ import annotations

from homeassistant.components.light import ATTR_BRIGHTNESS, ATTR_EFFECT, ATTR_RGB_COLOR, ColorMode, LightEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import ClockForgeEntity


def _read_path(data: dict, path: tuple[str, ...]):
    value = data
    for key in path:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


class ClockForgeLightingEntity(ClockForgeEntity, LightEntity):
    _effect_to_mode = {
        "Static": "1",
        "Rainbow": "2",
        "Breathe": "3",
        "KITT": "4",
        "Sparkle": "5",
    }

    _mode_to_effect = {value: key for key, value in _effect_to_mode.items()}

    def __init__(self, coordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry, "lighting", "Lighting")
        self._attr_icon = "mdi:led-strip-variant"
        self._attr_supported_color_modes = {ColorMode.RGB}
        self._attr_color_mode = ColorMode.RGB
        self._attr_effect_list = list(self._effect_to_mode.keys())

    @property
    def available(self) -> bool:
        return super().available and bool(_read_path(self.coordinator.data, ("capabilities", "lighting")))

    @property
    def is_on(self) -> bool:
        return bool(_read_path(self.coordinator.data, ("lighting", "enabled")))

    @property
    def brightness(self) -> int | None:
        value = _read_path(self.coordinator.data, ("lighting", "brightness"))
        if value is None:
            return None
        return int(value)

    @property
    def rgb_color(self) -> tuple[int, int, int] | None:
        red = _read_path(self.coordinator.data, ("lighting", "red"))
        green = _read_path(self.coordinator.data, ("lighting", "green"))
        blue = _read_path(self.coordinator.data, ("lighting", "blue"))
        if red is None or green is None or blue is None:
            return None
        return (int(red), int(green), int(blue))

    @property
    def effect(self) -> str | None:
        mode = _read_path(self.coordinator.data, ("settings", "lighting", "mode"))
        if mode is None:
            mode = _read_path(self.coordinator.data, ("lighting", "mode"))
        return self._mode_to_effect.get(str(mode))

    async def async_turn_on(self, **kwargs) -> None:
        payload: dict[str, str] = {"lighting_enabled": "true"}
        if (effect := kwargs.get(ATTR_EFFECT)) is not None:
            mapped = self._effect_to_mode.get(str(effect))
            if mapped is not None:
                payload["lighting_mode"] = mapped
        if (brightness := kwargs.get(ATTR_BRIGHTNESS)) is not None:
            payload["lighting_brightness"] = str(int(brightness))
        if (rgb := kwargs.get(ATTR_RGB_COLOR)) is not None:
            payload["lighting_red"] = str(int(rgb[0]))
            payload["lighting_green"] = str(int(rgb[1]))
            payload["lighting_blue"] = str(int(rgb[2]))
        await self.coordinator.async_save_settings(**payload)

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.async_save_settings(lighting_enabled="false")


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    async_add_entities([ClockForgeLightingEntity(coordinator, entry)])
