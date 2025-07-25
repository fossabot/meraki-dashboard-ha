"""Constants for the Meraki Dashboard integration."""

from typing import Final

# Domain constant
DOMAIN: Final = "meraki_dashboard"

# Integration name
DEFAULT_NAME: Final = "Meraki Dashboard"

# Device types
SENSOR_TYPE_MT: Final = "MT"  # Environmental sensors
SENSOR_TYPE_MR: Final = "MR"  # Wireless access points
SENSOR_TYPE_MS: Final = "MS"  # Switches
SENSOR_TYPE_MV: Final = "MV"  # Cameras

# Configuration keys
# Main configuration
CONF_API_KEY: Final = "api_key"
CONF_BASE_URL: Final = "base_url"
CONF_ORGANIZATION_ID: Final = "organization_id"
CONF_NETWORKS: Final = "networks"
CONF_SCAN_INTERVAL: Final = "scan_interval"
CONF_SELECTED_DEVICES: Final = "selected_devices"
CONF_AUTO_DISCOVERY: Final = "auto_discovery"
CONF_DISCOVERY_INTERVAL: Final = "discovery_interval"

# Per-hub configuration
CONF_HUB_SCAN_INTERVALS: Final = "hub_scan_intervals"
CONF_HUB_DISCOVERY_INTERVALS: Final = "hub_discovery_intervals"
CONF_HUB_AUTO_DISCOVERY: Final = "hub_auto_discovery"

# Tiered refresh configuration
CONF_STATIC_DATA_INTERVAL: Final = "static_data_interval"
CONF_SEMI_STATIC_DATA_INTERVAL: Final = "semi_static_data_interval"
CONF_DYNAMIC_DATA_INTERVAL: Final = "dynamic_data_interval"

# MT (Environmental) sensor metrics
MT_SENSOR_APPARENT_POWER: Final = "apparentPower"
MT_SENSOR_BATTERY: Final = "battery"
MT_SENSOR_BUTTON: Final = "button"
MT_SENSOR_CO2: Final = "co2"
MT_SENSOR_CURRENT: Final = "current"
MT_SENSOR_DOOR: Final = "door"
MT_SENSOR_DOWNSTREAM_POWER: Final = "downstreamPower"
MT_SENSOR_FREQUENCY: Final = "frequency"
MT_SENSOR_HUMIDITY: Final = "humidity"
MT_SENSOR_INDOOR_AIR_QUALITY: Final = "indoorAirQuality"
MT_SENSOR_NOISE: Final = "noise"
MT_SENSOR_PM25: Final = "pm25"
MT_SENSOR_POWER_FACTOR: Final = "powerFactor"
MT_SENSOR_REAL_POWER: Final = "realPower"
MT_SENSOR_REMOTE_LOCKOUT_SWITCH: Final = "remoteLockoutSwitch"
MT_SENSOR_TEMPERATURE: Final = "temperature"
MT_SENSOR_TVOC: Final = "tvoc"
MT_SENSOR_VOLTAGE: Final = "voltage"
MT_SENSOR_WATER: Final = "water"

# MR (Wireless) sensor metrics
MR_SENSOR_SSID_COUNT: Final = "ssid_count"
MR_SENSOR_ENABLED_SSIDS: Final = "enabled_ssids"
MR_SENSOR_OPEN_SSIDS: Final = "open_ssids"
MR_SENSOR_CLIENT_COUNT: Final = "client_count"
MR_SENSOR_MEMORY_USAGE: Final = "memory_usage"
# Channel utilization metrics for 2.4GHz
MR_SENSOR_CHANNEL_UTILIZATION_TOTAL_24: Final = "channel_utilization_total_24"
MR_SENSOR_CHANNEL_UTILIZATION_WIFI_24: Final = "channel_utilization_wifi_24"
MR_SENSOR_CHANNEL_UTILIZATION_NON_WIFI_24: Final = "channel_utilization_non_wifi_24"
# Channel utilization metrics for 5GHz
MR_SENSOR_CHANNEL_UTILIZATION_TOTAL_5: Final = "channel_utilization_total_5"
MR_SENSOR_CHANNEL_UTILIZATION_WIFI_5: Final = "channel_utilization_wifi_5"
MR_SENSOR_CHANNEL_UTILIZATION_NON_WIFI_5: Final = "channel_utilization_non_wifi_5"

# MS (Switch) sensor metrics
MS_SENSOR_PORT_COUNT: Final = "port_count"
MS_SENSOR_CONNECTED_PORTS: Final = "connected_ports"
MS_SENSOR_POE_PORTS: Final = "poe_ports"
MS_SENSOR_PORT_UTILIZATION_SENT: Final = "port_utilization_sent"
MS_SENSOR_PORT_UTILIZATION_RECV: Final = "port_utilization_recv"
MS_SENSOR_PORT_TRAFFIC_SENT: Final = "port_traffic_sent"
MS_SENSOR_PORT_TRAFFIC_RECV: Final = "port_traffic_recv"
MS_SENSOR_POE_POWER: Final = "poe_power"
MS_SENSOR_CONNECTED_CLIENTS: Final = "connected_clients"
MS_SENSOR_POWER_MODULE_STATUS: Final = "power_module_status"
MS_SENSOR_PORT_ERRORS: Final = "port_errors"
MS_SENSOR_PORT_DISCARDS: Final = "port_discards"
MS_SENSOR_PORT_LINK_COUNT: Final = "port_link_count"
MS_SENSOR_POE_LIMIT: Final = "poe_limit"
MS_SENSOR_PORT_UTILIZATION: Final = "port_utilization"
MS_SENSOR_MEMORY_USAGE: Final = "memory_usage"

# Organization-level metrics
ORG_SENSOR_API_CALLS: Final = "api_calls"
ORG_SENSOR_FAILED_API_CALLS: Final = "failed_api_calls"
ORG_SENSOR_DEVICE_COUNT: Final = "device_count"
ORG_SENSOR_NETWORK_COUNT: Final = "network_count"
ORG_SENSOR_OFFLINE_DEVICES: Final = "offline_devices"
ORG_SENSOR_ALERTS_COUNT: Final = "alerts_count"
ORG_SENSOR_LICENSE_EXPIRING: Final = "license_expiring"
ORG_SENSOR_CLIENTS_TOTAL_COUNT: Final = "clients_total_count"
ORG_SENSOR_CLIENTS_USAGE_OVERALL_TOTAL: Final = "clients_usage_overall_total"
ORG_SENSOR_CLIENTS_USAGE_OVERALL_DOWNSTREAM: Final = "clients_usage_overall_downstream"
ORG_SENSOR_CLIENTS_USAGE_OVERALL_UPSTREAM: Final = "clients_usage_overall_upstream"
ORG_SENSOR_CLIENTS_USAGE_AVERAGE_TOTAL: Final = "clients_usage_average_total"
ORG_SENSOR_BLUETOOTH_CLIENTS_TOTAL_COUNT: Final = "bluetooth_clients_total_count"
ORG_SENSOR_DEVICE_STATUS: Final = "device_status"
ORG_SENSOR_LICENSE_INVENTORY: Final = "license_inventory"
ORG_SENSOR_RECENT_ALERTS: Final = "recent_alerts"
ORG_SENSOR_UPLINK_STATUS: Final = "uplink_status"

# Hub types
HUB_TYPE_ORGANIZATION: Final = "organization"
HUB_TYPE_NETWORK: Final = "network"

# Entity attributes
ATTR_NETWORK_ID: Final = "network_id"
ATTR_NETWORK_NAME: Final = "network_name"
ATTR_SERIAL: Final = "serial"
ATTR_MODEL: Final = "model"
ATTR_LAST_REPORTED_AT: Final = "last_reported_at"

# Event configuration
EVENT_TYPE: Final = "meraki_dashboard_event"
EVENT_DEVICE_ID: Final = "device_id"
EVENT_DEVICE_SERIAL: Final = "device_serial"
EVENT_SENSOR_TYPE: Final = "sensor_type"
EVENT_VALUE: Final = "value"
EVENT_PREVIOUS_VALUE: Final = "previous_value"
EVENT_TIMESTAMP: Final = "timestamp"

# API Configuration
USER_AGENT: Final = "MerakiDashboardHomeAssistant rknightion"
DEFAULT_BASE_URL: Final = "https://api.meraki.com/api/v1"
REGIONAL_BASE_URLS: Final = {
    "Global": "https://api.meraki.com/api/v1",
    "Canada": "https://api.meraki.ca/api/v1",
    "China": "https://api.meraki.cn/api/v1",
    "India": "https://api.meraki.in/api/v1",
    "US Government": "https://api.gov-meraki.com/api/v1",
}

# Scan intervals (in seconds)
DEFAULT_SCAN_INTERVAL: Final = 300  # 5 minutes
MIN_SCAN_INTERVAL: Final = 60  # 1 minute
DEFAULT_DISCOVERY_INTERVAL: Final = 3600  # 1 hour
MIN_DISCOVERY_INTERVAL: Final = 300  # 5 minutes

# Device type specific intervals (in seconds)
DEVICE_TYPE_SCAN_INTERVALS: Final = {
    SENSOR_TYPE_MT: 600,  # 10 minutes for environmental sensors
    SENSOR_TYPE_MR: 300,  # 5 minutes for wireless access points
    SENSOR_TYPE_MS: 300,  # 5 minutes for switches
    SENSOR_TYPE_MV: 600,  # 10 minutes for cameras
}

# UI display intervals (in minutes)
DEFAULT_SCAN_INTERVAL_MINUTES: Final = {
    SENSOR_TYPE_MT: 10,
    SENSOR_TYPE_MR: 5,
    SENSOR_TYPE_MS: 5,
    SENSOR_TYPE_MV: 10,
}

DEFAULT_DISCOVERY_INTERVAL_MINUTES: Final = 60  # 1 hour
MIN_SCAN_INTERVAL_MINUTES: Final = 1
MIN_DISCOVERY_INTERVAL_MINUTES: Final = 5

# Tiered refresh intervals (in seconds)
STATIC_DATA_REFRESH_INTERVAL: Final = 14400  # 4 hours
STATIC_DATA_REFRESH_INTERVAL_MINUTES: Final = 240  # 4 hours
SEMI_STATIC_DATA_REFRESH_INTERVAL: Final = 3600  # 1 hour
SEMI_STATIC_DATA_REFRESH_INTERVAL_MINUTES: Final = 60  # 1 hour
DYNAMIC_DATA_REFRESH_INTERVAL: Final = 600  # 10 minutes
DYNAMIC_DATA_REFRESH_INTERVAL_MINUTES: Final = 10  # 10 minutes

# Data type classifications
STATIC_DATA_TYPES: Final = ["license_inventory", "device_statuses"]
SEMI_STATIC_DATA_TYPES: Final = ["network_info", "device_info"]
DYNAMIC_DATA_TYPES: Final = ["sensor_readings", "uplink_status"]

# Device type mappings
DEVICE_TYPE_MAPPINGS: Final = {
    SENSOR_TYPE_MT: {
        "name_suffix": "Environmental Sensor",
        "description": "Environmental monitoring sensors for temperature, humidity, air quality, etc.",
        "model_prefixes": ["MT"],
    },
    SENSOR_TYPE_MR: {
        "name_suffix": "Wireless Access Point",
        "description": "Wireless access points providing WiFi connectivity and network metrics",
        "model_prefixes": ["MR"],
    },
    SENSOR_TYPE_MS: {
        "name_suffix": "Switch",
        "description": "Network switches providing port status, PoE power, and traffic metrics",
        "model_prefixes": ["MS"],
    },
    SENSOR_TYPE_MV: {
        "name_suffix": "Camera",
        "description": "Security cameras providing video analytics and motion detection",
        "model_prefixes": ["MV"],
    },
}

# Sensor groupings
MT_POWER_SENSORS: Final = [
    MT_SENSOR_APPARENT_POWER,
    MT_SENSOR_REAL_POWER,
    MT_SENSOR_CURRENT,
    MT_SENSOR_VOLTAGE,
    MT_SENSOR_FREQUENCY,
    MT_SENSOR_POWER_FACTOR,
]

MT_BINARY_SENSOR_METRICS: Final = [
    MT_SENSOR_BUTTON,
    MT_SENSOR_DOOR,
    MT_SENSOR_DOWNSTREAM_POWER,
    MT_SENSOR_REMOTE_LOCKOUT_SWITCH,
    MT_SENSOR_WATER,
]

MT_EVENT_SENSOR_METRICS: Final = [
    MT_SENSOR_BUTTON,
    MT_SENSOR_DOOR,
    MT_SENSOR_WATER,
]

# Organization hub suffix
ORG_HUB_SUFFIX: Final = "Organisation"
