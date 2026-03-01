from __future__ import annotations

import logging
from functools import partial

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import ClockForgeApi
from .const import (
    DOMAIN,
    PLATFORMS,
    SERVICE_SYNC_TIME,
    SERVICE_TOGGLE_DISPLAY,
    SERVICE_WIFI_CONNECT,
    SERVICE_WIFI_DISCONNECT,
)
from .coordinator import ClockForgeCoordinator

SERVICE_SCHEMA = vol.Schema({vol.Required("entry_id"): str})


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["logger"] = logging.getLogger(__name__)

    if not hass.services.has_service(DOMAIN, SERVICE_SYNC_TIME):
        hass.services.async_register(DOMAIN, SERVICE_SYNC_TIME, partial(_async_handle_sync_time, hass), schema=SERVICE_SCHEMA)
        hass.services.async_register(DOMAIN, SERVICE_WIFI_CONNECT, partial(_async_handle_wifi_connect, hass), schema=SERVICE_SCHEMA)
        hass.services.async_register(DOMAIN, SERVICE_WIFI_DISCONNECT, partial(_async_handle_wifi_disconnect, hass), schema=SERVICE_SCHEMA)
        hass.services.async_register(DOMAIN, SERVICE_TOGGLE_DISPLAY, partial(_async_handle_toggle_display, hass), schema=SERVICE_SCHEMA)

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["logger"] = logging.getLogger(__name__)

    session = async_get_clientsession(hass)
    api = ClockForgeApi(
        entry.data[CONF_HOST],
        entry.data.get(CONF_USERNAME),
        entry.data.get(CONF_PASSWORD),
        session,
    )
    coordinator = ClockForgeCoordinator(hass, entry, api)
    await coordinator.async_config_entry_first_refresh()
    await coordinator.async_setup_runtime()

    entry.async_on_unload(entry.add_update_listener(_async_reload_entry))

    hass.data[DOMAIN][entry.entry_id] = {
        "api": api,
        "coordinator": coordinator,
    }
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    data = hass.data[DOMAIN].get(entry.entry_id)
    if data is not None:
        await data["coordinator"].async_shutdown_runtime()

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok


async def _async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)


def _coordinator_from_service(hass: HomeAssistant, call: ServiceCall) -> ClockForgeCoordinator:
    entry_id = call.data["entry_id"]
    return hass.data[DOMAIN][entry_id]["coordinator"]


async def _async_handle_sync_time(hass: HomeAssistant, call: ServiceCall) -> None:
    coordinator = _coordinator_from_service(hass, call)
    await coordinator.async_execute_command(mqtt_suffix="time/sync", http_action="sync")


async def _async_handle_wifi_connect(hass: HomeAssistant, call: ServiceCall) -> None:
    coordinator = _coordinator_from_service(hass, call)
    await coordinator.async_execute_command(mqtt_suffix="wifi/connect", http_action="wifi_connect")


async def _async_handle_wifi_disconnect(hass: HomeAssistant, call: ServiceCall) -> None:
    coordinator = _coordinator_from_service(hass, call)
    await coordinator.async_execute_command(mqtt_suffix="wifi/disconnect", http_action="wifi_disconnect")


async def _async_handle_toggle_display(hass: HomeAssistant, call: ServiceCall) -> None:
    coordinator = _coordinator_from_service(hass, call)
    await coordinator.async_execute_command(mqtt_suffix="display/set", http_action="display_toggle", mqtt_payload="toggle")
