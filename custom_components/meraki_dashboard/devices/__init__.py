"""Device-specific implementations for Meraki Dashboard integration."""

from .mr import MerakiMRDeviceSensor, MerakiMRSensor
from .ms import MerakiMSDeviceSensor, MerakiMSSensor
from .mt import MerakiMTEnergySensor, MerakiMTSensor
from .organization import (
    MerakiHubAlertsCountSensor,
    MerakiHubApiCallsSensor,
    MerakiHubBluetoothClientsTotalCountSensor,
    MerakiHubClientsTotalCountSensor,
    MerakiHubClientsUsageAverageTotalSensor,
    MerakiHubClientsUsageOverallDownstreamSensor,
    MerakiHubClientsUsageOverallTotalSensor,
    MerakiHubClientsUsageOverallUpstreamSensor,
    MerakiHubDeviceCountSensor,
    MerakiHubFailedApiCallsSensor,
    MerakiHubLicenseExpiringSensor,
    MerakiHubNetworkCountSensor,
    MerakiHubOfflineDevicesSensor,
    MerakiNetworkDeviceCountSensor,
)

__all__ = [
    "MerakiMTSensor",
    "MerakiMTEnergySensor",
    "MerakiMRSensor",
    "MerakiMRDeviceSensor",
    "MerakiMSSensor",
    "MerakiMSDeviceSensor",
    "MerakiHubAlertsCountSensor",
    "MerakiHubApiCallsSensor",
    "MerakiHubBluetoothClientsTotalCountSensor",
    "MerakiHubClientsTotalCountSensor",
    "MerakiHubClientsUsageAverageTotalSensor",
    "MerakiHubClientsUsageOverallDownstreamSensor",
    "MerakiHubClientsUsageOverallTotalSensor",
    "MerakiHubClientsUsageOverallUpstreamSensor",
    "MerakiHubDeviceCountSensor",
    "MerakiHubFailedApiCallsSensor",
    "MerakiHubLicenseExpiringSensor",
    "MerakiHubNetworkCountSensor",
    "MerakiHubOfflineDevicesSensor",
    "MerakiNetworkDeviceCountSensor",
]
