from datetime import timedelta

DOMAIN = "clockforgeos"
PLATFORMS = ["sensor", "binary_sensor", "button", "switch", "number", "select", "light"]

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
BUTTON_ALARM_STOP = "alarm_stop"
BUTTON_TOUCH_RECALIBRATE = "touch_recalibrate"
BUTTON_CATHODE_PROTECT = "cathode_protect"
BUTTON_RESTART = "restart"

SERVICE_SYNC_TIME = "sync_time"
SERVICE_WIFI_CONNECT = "wifi_connect"
SERVICE_WIFI_DISCONNECT = "wifi_disconnect"
SERVICE_TOGGLE_DISPLAY = "toggle_display"

SENSOR_DESCRIPTIONS = (
    ("temperature", "Temperature", ("sensors", "temperature"), "temperature", "C"),
    ("humidity", "Humidity", ("sensors", "humidity"), "humidity", "%"),
    ("pressure", "Pressure", ("sensors", "pressure"), "atmospheric_pressure", "hPa"),
    ("lux", "Illuminance", ("sensors", "lux"), "illuminance", "lx"),
    ("brightness", "Display Brightness", ("display", "brightness"), None, "%"),
    ("lighting_mode", "Lighting Mode", ("lighting", "mode"), None, None),
    ("ota_state", "OTA State", ("ota", "state"), None, None),
    ("ota_progress", "OTA Progress", ("ota", "progressPercent"), None, "%"),
    ("time_source", "Time Source", ("time", "source"), None, None),
    ("wifi_state", "WiFi State", ("network", "state"), None, None),
    ("mqtt_state", "MQTT State", ("network", "mqttState"), None, None),
    ("uptime", "Uptime", ("system", "uptimeSeconds"), "duration", "s"),
    ("free_heap", "Free Heap", ("system", "freeHeapBytes"), "data_size", "B"),
    ("min_free_heap", "Min Free Heap", ("system", "minFreeHeapBytes"), "data_size", "B"),
    ("wifi_rssi", "WiFi RSSI", ("system", "wifiRssiDbm"), "signal_strength", "dBm"),
    ("chip_temperature", "Chip Temperature", ("system", "chipTemperature"), "temperature", "C"),
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
    ("show_date", "Show Date", ("settings", "display", "showDate"), "mdi:calendar", None, "display_show_date"),
    ("show_temperature", "Show Temperature", ("settings", "display", "showTemperature"), "mdi:thermometer", None, "display_show_temperature"),
    ("show_humidity", "Show Humidity", ("settings", "display", "showHumidity"), "mdi:water-percent", None, "display_show_humidity"),
    ("show_pressure", "Show Pressure", ("settings", "display", "showPressure"), "mdi:gauge", None, "display_show_pressure"),
    ("blink_enabled", "Blink Separators", ("settings", "display", "blinkEnabled"), "mdi:dots-horizontal", None, "display_blink_enabled"),
    ("double_blink_enabled", "Double Blink", ("settings", "display", "doubleBlinkEnabled"), "mdi:dots-grid", None, "display_double_blink_enabled"),
    ("zero_pad_hours", "Zero Pad Hours", ("settings", "display", "zeroPadHours"), "mdi:numeric-0-box", None, "display_zero_pad_hours"),
    ("auto_night_mode", "Auto Night Mode", ("settings", "display", "autoNightModeEnabled"), "mdi:theme-light-dark", None, "display_auto_night_mode_enabled"),
    ("cathode_protection", "Cathode Protection", ("settings", "display", "cathodeProtectionEnabled"), "mdi:shield-sync", None, "display_cathode_protection_enabled"),
    ("alarm_enabled", "Alarm Enabled", ("settings", "alarm", "enabled"), "mdi:alarm", None, "alarm_enabled"),
    ("lighting_enabled", "Lighting Enabled", ("settings", "lighting", "enabled"), "mdi:led-strip-variant", None, "lighting_enabled"),
    ("lighting_night_off", "Lighting Night Off", ("settings", "lighting", "nightOff"), "mdi:weather-night", None, "lighting_night_off"),
    ("lighting_random_colors", "Lighting Random Colors", ("settings", "lighting", "randomColors"), "mdi:palette-swatch", None, "lighting_random_colors"),
    ("wifi_enabled", "WiFi Enabled", ("settings", "network", "wifiEnabled"), "mdi:wifi", None, "wifi_enabled"),
    ("mqtt_enabled", "MQTT Enabled", ("settings", "network", "mqttEnabled"), "mdi:message-processing", None, "mqtt_enabled"),
    ("ntp_enabled", "NTP Enabled", ("settings", "time", "ntpEnabled"), "mdi:clock-check-outline", None, "ntp_enabled"),
    ("rtc_enabled", "RTC Enabled", ("settings", "time", "rtcEnabled"), "mdi:calendar-clock", None, "rtc_enabled"),
    ("auto_dst_enabled", "Auto DST", ("settings", "time", "autoDstEnabled"), "mdi:weather-sunset-up", None, "time_auto_dst_enabled"),
    ("http_auth_enabled", "HTTP Auth Enabled", ("settings", "security", "httpAuthEnabled"), "mdi:lock-outline", None, "http_auth_enabled"),
    ("ota_enabled", "OTA Enabled", ("settings", "security", "otaEnabled"), "mdi:upload-network", None, "ota_enabled"),
)

NUMBER_DESCRIPTIONS = (
    ("display_brightness", "Display Brightness", ("settings", "display", "brightness"), 0, 100, 1, "%", "display_brightness", 1.0),
    ("date_repeat", "Date Repeat", ("settings", "display", "dateRepeatMin"), 0, 60, 1, "min", "display_date_repeat_min", 1.0),
    ("temp_repeat", "Temperature Repeat", ("settings", "display", "tempRepeatMin"), 0, 60, 1, "min", "display_temp_repeat_min", 1.0),
    ("humidity_repeat", "Humidity Repeat", ("settings", "display", "humidityRepeatMin"), 0, 60, 1, "min", "display_humidity_repeat_min", 1.0),
    ("pressure_repeat", "Pressure Repeat", ("settings", "display", "pressureRepeatMin"), 0, 60, 1, "min", "display_pressure_repeat_min", 1.0),
    ("tube_effect_mode", "Tube Effect Mode", ("settings", "display", "tubeEffectMode"), 0, 15, 1, None, "display_tube_effect_mode", 1.0),
    ("temperature_correction", "Temperature Correction", ("settings", "display", "temperatureCorrectionTenths"), -9.9, 9.9, 0.1, "C", "display_temperature_correction_tenths", 0.1),
    ("day_brightness", "Day Brightness", ("settings", "display", "dayBrightness"), 0, 100, 1, "%", "display_day_brightness", 1.0),
    ("night_brightness", "Night Brightness", ("settings", "display", "nightBrightness"), 0, 100, 1, "%", "display_night_brightness", 1.0),
    ("lux_night_threshold", "Lux Night Threshold", ("settings", "display", "luxNightThreshold"), 0, 100, 1, "lx", "display_lux_night_threshold", 1.0),
    ("lux_day_threshold", "Lux Day Threshold", ("settings", "display", "luxDayThreshold"), 0, 100, 1, "lx", "display_lux_day_threshold", 1.0),
    ("cathode_interval_hours", "Cathode Interval Hours", ("settings", "display", "cathodeProtectionIntervalHours"), 0, 168, 1, "h", "display_cathode_protection_interval_hours", 1.0),
    ("alarm_duration", "Alarm Duration", ("settings", "alarm", "periodSeconds"), 1, 240, 1, "s", "alarm_period_seconds", 1.0),
    ("lighting_speed", "Lighting Speed", ("settings", "lighting", "speed"), 1, 255, 1, None, "lighting_speed", 1.0),
    ("lighting_brightness", "Lighting Brightness", ("settings", "lighting", "brightness"), 0, 255, 1, None, "lighting_brightness", 1.0),
    ("lighting_red", "Lighting Red", ("settings", "lighting", "red"), 0, 255, 1, None, "lighting_red", 1.0),
    ("lighting_green", "Lighting Green", ("settings", "lighting", "green"), 0, 255, 1, None, "lighting_green", 1.0),
    ("lighting_blue", "Lighting Blue", ("settings", "lighting", "blue"), 0, 255, 1, None, "lighting_blue", 1.0),
    ("radar_timeout", "Radar Timeout", ("settings", "display", "radarTimeoutMin"), 0, 60, 1, "min", "radar_timeout_min", 1.0),
    ("utc_offset_hours", "UTC Offset Hours", ("settings", "time", "utcOffsetHours"), -12, 14, 1, "h", "utc_offset_hours", 1.0),
)

SELECT_DESCRIPTIONS = (
    ("date_mode", "Date Format", ("settings", "display", "dateMode"), {
        "0": "dd/mm/yy",
        "1": "mm/dd/yy",
        "2": "yy/mm/dd",
    }, "display_date_mode"),
    ("temperature_unit", "Temperature Unit", ("settings", "display", "tempUnitFahrenheit"), {
        "false": "Celsius",
        "true": "Fahrenheit",
    }, "display_temp_unit_fahrenheit"),
    ("lighting_mode", "Lighting Mode", ("settings", "lighting", "mode"), {
        "1": "Static",
        "2": "Rainbow",
        "3": "Breathe",
        "4": "KITT",
        "5": "Sparkle",
        "6": "Flow",
        "7": "Random",
        "8": "Fireworks",
    }, "lighting_mode"),
    ("touch_short_action", "Touch Short Action", ("settings", "touch", "shortAction"), {
        "0": "None",
        "1": "Alarm Off",
        "2": "Random Colors",
        "4": "Display Toggle",
    }, "touch_short_action"),
    ("touch_double_action", "Touch Double Action", ("settings", "touch", "doubleAction"), {
        "0": "None",
        "1": "Alarm Off",
        "2": "Random Colors",
        "4": "Display Toggle",
    }, "touch_double_action"),
    ("touch_long_action", "Touch Long Action", ("settings", "touch", "longAction"), {
        "0": "None",
        "1": "Alarm Off",
        "2": "Random Colors",
        "4": "Display Toggle",
    }, "touch_long_action"),
)

BUTTON_DESCRIPTIONS = (
    (BUTTON_SYNC, "Sync Time", "time/sync", "sync", None, None),
    (BUTTON_DISPLAY_TOGGLE, "Toggle Display", "display/set", "display_toggle", "toggle", None),
    (BUTTON_WIFI_CONNECT, "WiFi Connect", "wifi/connect", "wifi_connect", None, None),
    (BUTTON_WIFI_DISCONNECT, "WiFi Disconnect", "wifi/disconnect", "wifi_disconnect", None, None),
    (BUTTON_ALARM_STOP, "Stop Alarm", None, "alarm_stop", None, None),
    (BUTTON_TOUCH_RECALIBRATE, "Touch Recalibrate", None, "touch_recalibrate", None, None),
    (BUTTON_CATHODE_PROTECT, "Run Cathode Protect", None, "cathode_protect", None, None),
    (BUTTON_RESTART, "Restart Device", None, "restart", None, None),
)
