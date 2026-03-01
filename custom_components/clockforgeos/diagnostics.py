from __future__ import annotations

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DIAGNOSTICS_REDACT_KEYS, DOMAIN


async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: ConfigEntry) -> dict:
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]

    return {
        "entry": async_redact_data(dict(entry.as_dict()), DIAGNOSTICS_REDACT_KEYS),
        "status": async_redact_data(coordinator.data or {}, DIAGNOSTICS_REDACT_KEYS),
        "last_command_result": coordinator.last_command_result,
    }
