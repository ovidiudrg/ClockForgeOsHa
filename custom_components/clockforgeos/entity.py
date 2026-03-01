from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_LAST_COMMAND_RESULT,
    ATTR_MQTT_BASE_TOPIC,
    ATTR_MQTT_COMMAND_BASE,
    ATTR_MQTT_CORRELATION_IDS,
    ATTR_MQTT_CONTRACT_VERSION,
    ATTR_MQTT_RESULT_TOPIC,
    ATTR_PROFILE,
    DOMAIN,
)


class ClockForgeEntity(CoordinatorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, entry, key: str, name: str) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._key = key
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_name = name

    @property
    def device_info(self) -> DeviceInfo:
        status = self.coordinator.data
        profile = status.get("profile", "clockforge")
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name=f"ClockForgeOS {profile}",
            manufacturer="ClockForge",
            model=profile,
            sw_version="HACS Contract " + status.get("network", {}).get("mqttContractVersion", "unknown"),
        )

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        status = self.coordinator.data
        network = status.get("network", {})
        attributes = {
            ATTR_PROFILE: status.get("profile", ""),
            ATTR_MQTT_BASE_TOPIC: network.get("mqttBaseTopic", ""),
            ATTR_MQTT_COMMAND_BASE: network.get("mqttCommandBase", ""),
            ATTR_MQTT_RESULT_TOPIC: network.get("mqttResultTopic", ""),
            ATTR_MQTT_CONTRACT_VERSION: network.get("mqttContractVersion", ""),
            ATTR_MQTT_CORRELATION_IDS: network.get("mqttCorrelationIds", False),
        }
        if self.coordinator.last_command_result is not None:
            attributes[ATTR_LAST_COMMAND_RESULT] = self.coordinator.last_command_result
        return attributes
