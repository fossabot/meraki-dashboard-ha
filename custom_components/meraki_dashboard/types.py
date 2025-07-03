"""Type definitions for Meraki Dashboard integration."""
# ruff: noqa: N802, N803

from __future__ import annotations

from typing import Any, Protocol, TypedDict


# Device and API Response Types
class MerakiDeviceData(TypedDict, total=False):
    """Type definition for Meraki device data."""

    serial: str
    name: str
    model: str
    networkId: str
    mac: str | None
    lat: str | int | float | None
    lng: str | int | float | None
    address: str | None
    notes: str | None
    tags: str | list[str] | None
    lanIp: str | None
    configurationUpdatedAt: str | None
    firmware: str | None
    url: str | None


# Sensor metric value types
class TemperatureReading(TypedDict):
    """Temperature sensor reading."""
    celsius: float
    fahrenheit: float | None


class HumidityReading(TypedDict):
    """Humidity sensor reading."""
    relativePercentage: float


class ConcentrationReading(TypedDict):
    """Concentration-based sensor reading (CO2, PM2.5, TVOC)."""
    concentration: float


class BatteryReading(TypedDict):
    """Battery sensor reading."""
    percentage: float


class PowerReading(TypedDict):
    """Power sensor reading."""
    value: float
    unit: str  # "W", "kW", "mW"
    draw: float | None  # Alternative field


class ElectricalReading(TypedDict):
    """Electrical measurement reading (voltage, current, etc)."""
    value: float
    unit: str | None


class NoiseReading(TypedDict, total=False):
    """Noise sensor reading with multiple possible formats."""
    ambient: float | None
    concentration: float | None
    level: float | dict[str, float] | None


class AirQualityReading(TypedDict):
    """Indoor air quality reading."""
    score: int


class BinarySensorReading(TypedDict):
    """Binary sensor reading (door, water, button)."""
    open: bool
    detected: bool | None
    pressed: bool | None


class SensorReading(TypedDict, total=False):
    """Type definition for sensor readings."""

    ts: str
    metric: str
    value: float | None
    temperature: TemperatureReading | None
    humidity: HumidityReading | None
    co2: ConcentrationReading | None
    battery: BatteryReading | None
    realPower: PowerReading | None
    apparentPower: PowerReading | None
    voltage: ElectricalReading | None
    current: ElectricalReading | None
    frequency: ElectricalReading | None
    powerFactor: ElectricalReading | None
    pm25: ConcentrationReading | None
    tvoc: ConcentrationReading | None
    noise: NoiseReading | float | None
    indoorAirQuality: AirQualityReading | None
    button: BinarySensorReading | None
    door: BinarySensorReading | None
    water: BinarySensorReading | None
    remoteLockoutSwitch: BinarySensorReading | None
    downstreamPower: BinarySensorReading | None


class MTDeviceData(TypedDict, total=False):
    """Type definition for MT device sensor data."""

    serial: str
    readings: list[SensorReading]


class NetworkData(TypedDict, total=False):
    """Type definition for network data."""

    id: str
    organizationId: str
    name: str
    productTypes: list[str]
    timeZone: str
    tags: list[str] | None
    enrollmentString: str | None
    url: str | None
    notes: str | None


class OrganizationData(TypedDict, total=False):
    """Type definition for organization data."""

    id: str
    name: str
    url: str | None
    api: dict[str, Any] | None
    licensing: dict[str, Any] | None
    cloud: dict[str, Any] | None


class DeviceStatus(TypedDict, total=False):
    """Type definition for device status."""

    serial: str
    name: str
    status: str
    lastReportedAt: str | None
    productType: str
    model: str
    networkId: str
    publicIp: str | None
    mac: str | None
    lanIp: str | None
    gateway: str | None
    ipType: str | None
    primaryDns: str | None
    secondaryDns: str | None
    usingCellularFailover: bool | None


class LicenseInfo(TypedDict, total=False):
    """Type definition for license information."""

    id: str
    licenseType: str
    licenseKey: str
    orderNumber: str | None
    deviceSerial: str | None
    networkId: str | None
    state: str
    seatCount: int | None
    totalDurationInDays: int | None
    durationInDays: int | None
    permanentlyQueuedLicenses: list[dict[str, Any]] | None
    claimDate: str | None
    activationDate: str | None


class UplinkStatus(TypedDict, total=False):
    """Type definition for uplink status."""

    networkId: str
    serial: str
    model: str
    lastReportedAt: str
    uplinks: list[dict[str, Any]]


class WirelessStats(TypedDict, total=False):
    """Type definition for wireless statistics."""

    serial: str
    model: str
    clientCount: int | None
    basicServiceSets: list[dict[str, Any]] | None
    connectionStats: dict[str, Any] | list[dict[str, Any]] | None
    channelUtilization24: float | None
    channelUtilization5: float | None
    dataRate24: float | None
    dataRate5: float | None
    trafficSent: float | None
    trafficRecv: float | None
    rfPower: float | None
    rfPower24: float | None
    rfPower5: float | None
    radioChannel24: int | None
    radioChannel5: int | None
    channelWidth5: int | None
    rfProfileId: str | None


class SwitchPortStatus(TypedDict, total=False):
    """Type definition for switch port status."""

    portId: str
    enabled: bool
    status: str
    errors: list[str]
    warnings: list[str]
    speed: str | None
    duplex: str | None
    usageInKb: dict[str, float] | None
    powerUsageInWh: float | None
    linkNegotiation: dict[str, Any] | None
    clientCount: int | None
    poeEnabled: bool | None
    rstpRole: str | None
    rstpState: str | None
    spanningTreePortState: str | None
    device_serial: str | None  # Added for aggregation


class SwitchStats(TypedDict, total=False):
    """Type definition for switch statistics."""

    serial: str
    model: str
    ports: list[SwitchPortStatus]
    portsStatus: list[SwitchPortStatus] | None  # Alternative format
    powerModules: list[dict[str, Any]] | None
    port_count: int | None
    connected_ports: int | None
    poe_ports: int | None
    connected_clients: int | None
    poe_power_draw: float | None
    port_utilization: float | None
    port_errors: int | None
    port_discards: int | None
    port_link_count: int | None


class MemoryUsageData(TypedDict, total=False):
    """Type definition for memory usage data."""

    serial: str
    freeInKb: float | None
    usedInKb: float | None
    memory_usage_percent: float | None


# Coordinator Data Types - Device-specific structures
class MTCoordinatorData(TypedDict):
    """Coordinator data structure for MT (Environmental) devices.

    Structure: {device_serial: device_data}
    """
    # Dynamic keys - each key is a device serial number
    # Value is the device's sensor data
    __root__: dict[DeviceSerial, MTDeviceData]


class MRCoordinatorData(TypedDict, total=False):
    """Coordinator data structure for MR (Wireless) devices."""

    devices_info: list[WirelessStats]
    ssids: list[dict[str, Any]]
    memory_usage: list[MemoryUsageData]


class MSCoordinatorData(TypedDict, total=False):
    """Coordinator data structure for MS (Switch) devices."""

    devices_info: list[SwitchStats]
    ports_status: list[SwitchPortStatus]
    power_modules: list[dict[str, Any]]
    memory_usage: list[MemoryUsageData]


class OrganizationCoordinatorData(TypedDict, total=False):
    """Coordinator data structure for organization-level data."""

    device_statuses: list[DeviceStatus]
    license_inventory: list[LicenseInfo]
    uplink_status: list[UplinkStatus]
    alerts: list[dict[str, Any]]
    api_usage: dict[str, Any]
    networks: list[NetworkData]
    organization_data: dict[str, Any]


# Type aliases for clarity
DeviceSerial = str

# Union type for all coordinator data types
CoordinatorData = (
    dict[DeviceSerial, MTDeviceData] |  # MT devices use serial as key
    MRCoordinatorData |
    MSCoordinatorData |
    OrganizationCoordinatorData |
    dict[str, Any]  # Fallback for legacy code
)


# Protocol Types for API interfaces
class MerakiApiClient(Protocol):
    """Protocol for Meraki API client."""

    def organizations(self) -> dict[str, Any]:
        """Get organizations API endpoints."""
        ...

    def networks(self) -> dict[str, Any]:
        """Get networks API endpoints."""
        ...

    def devices(self) -> dict[str, Any]:
        """Get devices API endpoints."""
        ...

    def sensor(self) -> dict[str, Any]:
        """Get sensor API endpoints."""
        ...


class OrganizationApi(Protocol):
    """Protocol for organization API endpoints."""

    def getOrganizationDevices(
        self, organizationId: str, **kwargs
    ) -> list[MerakiDeviceData]:
        """Get organization devices."""
        ...

    def getOrganizationDevicesStatuses(
        self, organizationId: str, **kwargs
    ) -> list[DeviceStatus]:
        """Get organization device statuses."""
        ...

    def getOrganizationLicensesOverview(
        self, organizationId: str, **kwargs
    ) -> dict[str, Any]:
        """Get organization licenses overview."""
        ...

    def getOrganizationSensorReadingsLatest(
        self, organizationId: str, **kwargs
    ) -> dict[str, list[MTDeviceData]]:
        """Get latest sensor readings."""
        ...

    def getOrganizationDevicesUplinksAddressesByDevice(
        self, organizationId: str, **kwargs
    ) -> list[UplinkStatus]:
        """Get uplink addresses by device."""
        ...


class NetworkApi(Protocol):
    """Protocol for network API endpoints."""

    def getNetworkDevices(self, networkId: str) -> list[MerakiDeviceData]:
        """Get network devices."""
        ...

    def getNetworkWirelessDevicesConnectionStats(
        self, networkId: str, **kwargs
    ) -> list[WirelessStats]:
        """Get wireless connection stats."""
        ...

    def getNetworkSwitchPortsStatuses(
        self, networkId: str, **kwargs
    ) -> list[SwitchPortStatus]:
        """Get switch port statuses."""
        ...

    def getNetworkWirelessSsids(self, networkId: str) -> list[dict[str, Any]]:
        """Get wireless SSIDs."""
        ...


class DeviceApi(Protocol):
    """Protocol for device API endpoints."""

    def getDeviceSwitchPortsStatuses(self, serial: str) -> list[SwitchPortStatus]:
        """Get device switch port statuses."""
        ...


class SensorApi(Protocol):
    """Protocol for sensor API endpoints."""

    def getDeviceSensorReadingsLatest(self, serial: str) -> list[SensorReading]:
        """Get latest sensor readings for device."""
        ...


# Hub and Coordinator Interface Types
class NetworkHubProtocol(Protocol):
    """Protocol for network hub interface."""

    network_id: str
    network_name: str
    device_type: str
    devices: list[MerakiDeviceData]

    async def async_update_devices_info(self) -> list[WirelessStats | SwitchStats]:
        """Update devices info."""
        ...


class OrganizationHubProtocol(Protocol):
    """Protocol for organization hub interface."""

    organization_id: str
    organization_name: str
    device_statuses: list[DeviceStatus]
    license_data: dict[str, Any]
    device_memory_usage: dict[str, MemoryUsageData]

    async def async_update_organization_data(self) -> dict[str, Any]:
        """Update organization data."""
        ...


# Configuration Types
class HubConfiguration(TypedDict, total=False):
    """Type definition for hub configuration."""

    scan_interval: int
    discovery_interval: int
    auto_discovery: bool


class IntegrationConfig(TypedDict, total=False):
    """Type definition for integration configuration."""

    api_key: str
    organization_id: str
    base_url: str
    scan_intervals: dict[str, int]
    discovery_intervals: dict[str, int]
    hub_configs: dict[str, HubConfiguration]
    auto_discovery: bool


# Error and Response Types
class ApiErrorResponse(TypedDict, total=False):
    """Type definition for API error responses."""

    errors: list[str]
    message: str | None
    status: int | None


# Union types for common use cases
DeviceDataUnion = MerakiDeviceData | WirelessStats | SwitchStats
ApiResponseUnion = list[Any] | dict[str, Any]
SensorDataUnion = SensorReading | MTDeviceData

# Type aliases for clarity
NetworkId = str
OrganizationId = str
EntityId = str
