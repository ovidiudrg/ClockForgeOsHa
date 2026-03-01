# ClockForgeOS Home Assistant Integration

This custom integration is the first HACS-facing client for `ClockForgeOS`.

## Current Scope

1. Add a clock through its local HTTP API.
2. Poll `/api/status` for device state and capabilities.
3. Expose sensors, binary sensors, control buttons, switches, numbers, and a light entity in Home Assistant.
4. Expose service calls for sync, Wi-Fi connect/disconnect, and display toggle.
5. Consume the firmware MQTT command/result contract when enabled, including request/result correlation IDs.
6. Expose config-entry options and diagnostics for support workflows.

## Install

1. Copy `custom_components/clockforgeos` into your Home Assistant `custom_components` directory.
2. Keep `hacs.json` in the repository root when publishing the integration repo.
3. Restart Home Assistant.
4. Add `ClockForgeOS` from the integrations UI.

## Config Entry

Initial setup uses:

1. Clock host or IP
2. Optional HTTP username
3. Optional HTTP password

Options flow adds:

1. `Control transport`
   `auto`: prefer MQTT when the device publishes a command base, otherwise fall back to HTTP.
   `http`: force HTTP control calls.
   `mqtt`: require MQTT command publishing.
2. `Status poll interval (seconds)`

## HACS Contract v2

The integration discovers the firmware contract from `/api/status`.

Expected status fields:

1. `network.mqttBaseTopic`
2. `network.mqttCommandBase`
3. `network.mqttResultTopic`
4. `network.mqttContractVersion`
5. `network.mqttCorrelationIds`

Current command topics:

1. `<commandBase>/time/sync`
2. `<commandBase>/display/set`
3. `<commandBase>/wifi/connect`
4. `<commandBase>/wifi/disconnect`

Current result topic:

1. `<mqttResultTopic>`

Expected result payload shape:

```json
{
  "contract": "v2",
  "command": "time/sync",
  "requestId": "9c4a4f6c2b764e07b70ec6f2fd6c4fc0",
  "ok": true,
  "detail": "queued"
}
```

## Diagnostics

The integration exports:

1. redacted config-entry data
2. latest device status payload
3. latest command result payload

## Services

The integration currently registers:

1. `clockforgeos.sync_time`
2. `clockforgeos.wifi_connect`
3. `clockforgeos.wifi_disconnect`
4. `clockforgeos.toggle_display`

Each service currently takes `entry_id`.

## Control Entities

Current writable entities map to the firmware settings surface:

1. Switches:
   `Display Enabled`, `Wake On Motion`, `Lighting Enabled`, `WiFi Enabled`, `MQTT Enabled`, `NTP Enabled`, `RTC Enabled`, `OTA Enabled`
2. Numbers:
   `Display Brightness`, `Lighting Brightness`, `Lighting Red`, `Lighting Green`, `Lighting Blue`, `Radar Timeout`, `UTC Offset Hours`
3. Light:
   `Lighting`

Additional OTA observability:

1. Sensor: `OTA State`
2. Sensor: `OTA Progress`

There is no `select` entity yet because the current firmware API does not expose a stable device-backed enum setting that would justify one.

## Next

1. Map more firmware commands into Home Assistant services and entities.
2. Add integration tests once a Python-capable environment is available.
3. Add config-entry diagnostics for MQTT round-trip failures seen in real HA deployments.
