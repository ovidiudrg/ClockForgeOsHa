from datetime import timedelta

DOMAIN = "clockforgeos"
PLATFORMS = ["sensor", "binary_sensor", "button", "switch", "number"]

CONF_HTTP_USER = "http_user"
CONF_HTTP_PASSWORD = "http_password"
CONF_CONTROL_TRANSPORT = "control_transport"
CONF_SCAN_INTERVAL = "scan_interval"

CONTROL_TRANSPORT_AUTO = "auto"
CONTROL_TRANSPORT_HTTP = "http"
CONTROL_TRANSPORT_MQTT = "mqtt"

DEFAULT_SCAN_INTERVAL = timedelta(seconds=10)
DEFAULT_SCAN_INTERVAL_SECONDS = 10
DEFAULT_CONTROL_TRANSPORT = CONTROL_TRANSPORT_AUTO

ATTR_PROFILE = "profile"
ATTR_MQTT_BASE_TOPIC = "mqtt_base_topic"
ATTR_MQTT_COMMAND_BASE = "mqtt_command_base"
ATTR_MQTT_RESULT_TOPIC = "mqtt_result_topic"
ATTR_MQTT_CONTRACT_VERSION = "mqtt_contract_version"
ATTR_MQTT_CORRELATION_IDS = "mqtt_correlation_ids"
ATTR_LAST_COMMAND_RESULT = "last_command_result"

DIAGNOSTICS_REDACT_KEYS = {
    CONF_HTTP_PASSWORD,
    "password",
    "http_password",
    "mqttPassword",
}

BUTTON_SYNC = "sync_time"
BUTTON_DISPLAY_TOGGLE = "display_toggle"
BUTTON_WIFI_CONNECT = "wifi_connect"
BUTTON_WIFI_DISCONNECT = "wifi_disconnect"

SERVICE_SYNC_TIME = "sync_time"
SERVICE_WIFI_CONNECT = "wifi_connect"
SERVICE_WIFI_DISCONNECT = "wifi_disconnect"
SERVICE_TOGGLE_DISPLAY = "toggle_display"

SENSOR_DESCRIPTIONS = (
    ("temperature", "Temperature", ("sensors", "temperature"), "temperature", "°C"),
    ("humidity", "Humidity", ("sensors", "humidity"), "humidity", "%"),
    ("pressure", "Pressure", ("sensors", "pressure"), "atmospheric_pressure", "hPa"),
    ("lux", "Illuminance", ("sensors", "lux"), "illuminance", "lx"),
    ("brightness", "Display Brightness", ("display", "brightness"), None, "%"),
    ("time_source", "Time Source", ("time", "source"), None, None),
    ("wifi_state", "WiFi State", ("network", "state"), None, None),
    ("mqtt_state", "MQTT State", ("network", "mqttState"), None, None),
    ("uptime", "Uptime", ("system", "uptimeSeconds"), "duration", "s"),
    ("free_heap", "Free Heap", ("system", "freeHeapBytes"), "data_size", "B"),
    ("min_free_heap", "Min Free Heap", ("system", "minFreeHeapBytes"), "data_size", "B"),
    ("wifi_rssi", "WiFi RSSI", ("system", "wifiRssiDbm"), "signal_strength", "dBm"),
    ("chip_temperature", "Chip Temperature", ("system", "chipTemperature"), "temperature", "°C"),
    ("cpu_freq", "CPU Frequency", ("hardware", "cpuFreqMHz"), None, "MHz"),
    ("flash_size", "Flash Size", ("hardware", "flashSizeBytes"), "data_size", "B"),
    ("chip_revision", "Chip Revision", ("hardware", "chipRevision"), None, None),
    ("chip_model", "Chip Model", ("hardware", "chipModel"), None, None),
)

BINARY_SENSOR_DESCRIPTIONS = (
    ("motion", "Motion", ("sensors", "motion"), "motion"),
    ("occupancy", "Occupancy", ("sensors", "occupancy"), "occupancy"),
    ("wifi_connected", "WiFi Connected", ("network", "connected"), "connectivity"),
    ("mqtt_connected", "MQTT Connected", ("network", "mqttConnected"), "connectivity"),
)

SWITCH_DESCRIPTIONS = (
    ("display_enabled", "Display Enabled", ("settings", "display", "enabled"), "mdi:power", None, "display_enabled"),
    ("wake_on_motion", "Wake On Motion", ("settings", "display", "wakeOnMotionEnabled"), "mdi:motion-sensor", None, "wake_on_motion_enabled"),
    ("wifi_enabled", "WiFi Enabled", ("settings", "network", "wifiEnabled"), "mdi:wifi", None, "wifi_enabled"),
    ("mqtt_enabled", "MQTT Enabled", ("settings", "network", "mqttEnabled"), "mdi:message-processing", None, "mqtt_enabled"),
    ("ntp_enabled", "NTP Enabled", ("settings", "time", "ntpEnabled"), "mdi:clock-check-outline", None, "ntp_enabled"),
    ("rtc_enabled", "RTC Enabled", ("settings", "time", "rtcEnabled"), "mdi:calendar-clock", None, "rtc_enabled"),
)

NUMBER_DESCRIPTIONS = (
    ("display_brightness", "Display Brightness", ("settings", "display", "brightness"), 0, 100, 1, "%", "display_brightness"),
    ("radar_timeout", "Radar Timeout", ("settings", "display", "radarTimeoutMin"), 0, 60, 1, "min", "radar_timeout_min"),
    ("utc_offset_hours", "UTC Offset Hours", ("settings", "time", "utcOffsetHours"), -12, 14, 1, "h", "utc_offset_hours"),
)
