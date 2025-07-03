"""Entity factory for Meraki Dashboard integration.

This module provides a comprehensive factory pattern for creating all entity types
in the Meraki Dashboard integration. It handles device discovery, capability detection,
and entity instantiation for all supported device types.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any, TypeVar, cast

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.helpers.entity import Entity

from ..const import DeviceType
from ..const import EntityType as MetricType
from ..coordinator import MerakiSensorCoordinator

_LOGGER = logging.getLogger(__name__)

# Type variable for entity types
EntityT = TypeVar("EntityT", bound=Entity)


class EntityFactory:
    """Factory for creating Meraki entities with decorator-based registration.

    This factory provides:
    - Registration of entity creation functions by device type and metric type
    - Discovery of available entities for a device
    - Batch entity creation for devices
    - Type-safe entity instantiation
    """

    _registry: dict[str, Callable[..., Entity]] = {}
    _device_capabilities: dict[str, list[MetricType]] = {}

    @classmethod
    def register(cls, device_type: DeviceType, entity_type: MetricType) -> Callable:
        """Decorator to register entity creation functions.

        Args:
            device_type: The device type (MT, MR, MS, MV)
            entity_type: The metric/entity type (temperature, humidity, etc.)
        """
        def decorator(func: Callable[..., EntityT]) -> Callable[..., EntityT]:
            key = f"{device_type}_{entity_type}"
            cls._registry[key] = func

            # Track device capabilities
            if device_type not in cls._device_capabilities:
                cls._device_capabilities[device_type] = []
            if entity_type not in cls._device_capabilities[device_type]:
                cls._device_capabilities[device_type].append(entity_type)

            return func
        return decorator

    @classmethod
    def create_entity(
        cls,
        device_type: DeviceType,
        entity_type: MetricType,
        *args,
        **kwargs,
    ) -> Entity:
        """Create an entity of the specified type.

        Args:
            device_type: The device type
            entity_type: The metric/entity type
            *args: Positional arguments for entity constructor
            **kwargs: Keyword arguments for entity constructor

        Returns:
            The created entity instance

        Raises:
            ValueError: If the entity type is not registered
        """
        key = f"{device_type}_{entity_type}"
        if key not in cls._registry:
            raise ValueError(f"Unknown entity type: {key}")

        try:
            return cls._registry[key](*args, **kwargs)
        except Exception as e:
            _LOGGER.error("Failed to create entity %s: %s", key, e)
            raise

    @classmethod
    def create_entities(
        cls,
        coordinator: MerakiSensorCoordinator,
        device_data: dict[str, Any],
        config_entry_id: str,
    ) -> list[Entity]:
        """Create all applicable entities for a device.

        This method:
        1. Determines device type from device data
        2. Checks device capabilities against sensor readings
        3. Creates all supported entities

        Args:
            coordinator: The data coordinator
            device_data: Device information and sensor data
            config_entry_id: Config entry ID

        Returns:
            List of created entities
        """
        entities: list[Entity] = []
        device_type = cls._get_device_type(device_data)

        if not device_type:
            _LOGGER.warning("Could not determine device type for %s", device_data.get("serial"))
            return entities

        # Get available metrics for this device
        available_metrics = cls._get_available_metrics(device_type, device_data)

        for metric_type in available_metrics:
            try:
                entity = cls.create_entity(
                    device_type,
                    metric_type,
                    coordinator,
                    device_data,
                    config_entry_id
                )
                entities.append(entity)
            except Exception as e:
                _LOGGER.error(
                    "Failed to create %s entity for device %s: %s",
                    metric_type,
                    device_data.get("serial"),
                    e
                )

        return entities

    @classmethod
    def _get_device_type(cls, device_data: dict[str, Any]) -> DeviceType | None:
        """Determine device type from device data."""
        model = device_data.get("model", "")

        if model.startswith("MT"):
            return DeviceType.MT
        elif model.startswith("MR"):
            return DeviceType.MR
        elif model.startswith("MS"):
            return DeviceType.MS
        elif model.startswith("MV"):
            return DeviceType.MV

        return None

    @classmethod
    def _get_available_metrics(
        cls,
        device_type: DeviceType,
        device_data: dict[str, Any]
    ) -> list[MetricType]:
        """Get available metrics for a device based on its capabilities."""
        # Start with all registered metrics for this device type
        potential_metrics = cls._device_capabilities.get(device_type, [])
        available_metrics = []

        # Check each metric against device capabilities
        sensor_data = device_data.get("sensor", {})

        for metric in potential_metrics:
            # Check if device reports this metric
            if metric in sensor_data:
                available_metrics.append(metric)
            # Special cases for derived metrics
            elif metric == MetricType.INDOOR_AIR_QUALITY and "tvoc" in sensor_data:
                available_metrics.append(metric)
            # Add more special cases as needed

        return available_metrics

    @classmethod
    def get_registered_types(cls) -> list[str]:
        """Get list of all registered entity types."""
        return list(cls._registry.keys())

    @classmethod
    def get_device_capabilities(cls, device_type: DeviceType) -> list[MetricType]:
        """Get all possible capabilities for a device type."""
        return cls._device_capabilities.get(device_type, [])

    @classmethod
    def is_registered(cls, device_type: DeviceType, entity_type: MetricType) -> bool:
        """Check if an entity type is registered for a device type."""
        return f"{device_type}_{entity_type}" in cls._registry


# Import and register all entity types (using lazy imports to avoid circular imports)
def _register_mt_entities():
    """Register MT (Environmental) sensor entities."""

    # Temperature sensor
    @EntityFactory.register(DeviceType.MT, MetricType.TEMPERATURE)
    def create_mt_temperature(coordinator, device, config_entry_id, network_hub=None):
        from ..devices.mt import MerakiMTSensor
        from ..sensor import MT_SENSOR_DESCRIPTIONS
        return MerakiMTSensor(
            coordinator,
            device,
            MT_SENSOR_DESCRIPTIONS["temperature"],
            config_entry_id,
            network_hub
        )

    # Humidity sensor
    @EntityFactory.register(DeviceType.MT, MetricType.HUMIDITY)
    def create_mt_humidity(coordinator, device, config_entry_id, network_hub=None):
        from ..devices.mt import MerakiMTSensor
        from ..sensor import MT_SENSOR_DESCRIPTIONS
        return MerakiMTSensor(
            coordinator,
            device,
            MT_SENSOR_DESCRIPTIONS["humidity"],
            config_entry_id,
            network_hub
        )

    # CO2 sensor
    @EntityFactory.register(DeviceType.MT, MetricType.CO2)
    def create_mt_co2(coordinator, device, config_entry_id, network_hub=None):
        from ..devices.mt import MerakiMTSensor
        from ..sensor import MT_SENSOR_DESCRIPTIONS
        return MerakiMTSensor(
            coordinator,
            device,
            MT_SENSOR_DESCRIPTIONS["co2"],
            config_entry_id,
            network_hub
        )

    # TVOC sensor
    @EntityFactory.register(DeviceType.MT, MetricType.TVOC)
    def create_mt_tvoc(coordinator, device, config_entry_id, network_hub=None):
        from ..devices.mt import MerakiMTSensor
        from ..sensor import MT_SENSOR_DESCRIPTIONS
        return MerakiMTSensor(
            coordinator,
            device,
            MT_SENSOR_DESCRIPTIONS["tvoc"],
            config_entry_id,
            network_hub
        )

    # PM2.5 sensor
    @EntityFactory.register(DeviceType.MT, MetricType.PM25)
    def create_mt_pm25(coordinator, device, config_entry_id, network_hub=None):
        from ..devices.mt import MerakiMTSensor
        from ..sensor import MT_SENSOR_DESCRIPTIONS
        return MerakiMTSensor(
            coordinator,
            device,
            MT_SENSOR_DESCRIPTIONS["pm25"],
            config_entry_id,
            network_hub
        )

    # Noise sensor
    @EntityFactory.register(DeviceType.MT, MetricType.NOISE)
    def create_mt_noise(coordinator, device, config_entry_id, network_hub=None):
        from ..devices.mt import MerakiMTSensor
        from ..sensor import MT_SENSOR_DESCRIPTIONS
        return MerakiMTSensor(
            coordinator,
            device,
            MT_SENSOR_DESCRIPTIONS["noise"],
            config_entry_id,
            network_hub
        )

    # Indoor Air Quality sensor
    @EntityFactory.register(DeviceType.MT, MetricType.INDOOR_AIR_QUALITY)
    def create_mt_iaq(coordinator, device, config_entry_id, network_hub=None):
        from ..devices.mt import MerakiMTSensor
        from ..sensor import MT_SENSOR_DESCRIPTIONS
        return MerakiMTSensor(
            coordinator,
            device,
            MT_SENSOR_DESCRIPTIONS["indoorAirQuality"],
            config_entry_id,
            network_hub
        )

    # Battery sensor
    @EntityFactory.register(DeviceType.MT, MetricType.BATTERY)
    def create_mt_battery(coordinator, device, config_entry_id, network_hub=None):
        from ..devices.mt import MerakiMTSensor
        from ..sensor import MT_SENSOR_DESCRIPTIONS
        return MerakiMTSensor(
            coordinator,
            device,
            MT_SENSOR_DESCRIPTIONS["battery"],
            config_entry_id,
            network_hub
        )

    # Binary sensors for MT devices
    @EntityFactory.register(DeviceType.MT, MetricType.WATER)
    def create_mt_water_binary(coordinator, device, config_entry_id, network_hub=None):
        from ..binary_sensor import MT_BINARY_SENSOR_DESCRIPTIONS
        from ..devices.mt import MerakiMTBinarySensor
        return MerakiMTBinarySensor(
            coordinator,
            device,
            MT_BINARY_SENSOR_DESCRIPTIONS["water"],
            config_entry_id,
            network_hub
        )

    @EntityFactory.register(DeviceType.MT, MetricType.DOOR)
    def create_mt_door_binary(coordinator, device, config_entry_id, network_hub=None):
        from ..binary_sensor import MT_BINARY_SENSOR_DESCRIPTIONS
        from ..devices.mt import MerakiMTBinarySensor
        return MerakiMTBinarySensor(
            coordinator,
            device,
            MT_BINARY_SENSOR_DESCRIPTIONS["door"],
            config_entry_id,
            network_hub
        )


def _register_mr_entities():
    """Register MR (Wireless) sensor entities."""

    # MR device sensors
    @EntityFactory.register(DeviceType.MR, MetricType.CLIENT_COUNT)
    def create_mr_client_count(coordinator, device, config_entry_id, network_hub=None):
        from ..devices.mr import MerakiMRDeviceSensor
        from ..sensor import MR_SENSOR_DESCRIPTIONS
        return MerakiMRDeviceSensor(
            device,
            coordinator,
            MR_SENSOR_DESCRIPTIONS["client_count"],
            config_entry_id,
            network_hub
        )

    @EntityFactory.register(DeviceType.MR, MetricType.MEMORY_USAGE)
    def create_mr_memory_usage(coordinator, device, config_entry_id, network_hub=None):
        from ..devices.mr import MerakiMRDeviceSensor
        from ..sensor import MR_SENSOR_DESCRIPTIONS
        return MerakiMRDeviceSensor(
            device,
            coordinator,
            MR_SENSOR_DESCRIPTIONS["memoryUsage"],
            config_entry_id,
            network_hub
        )

    # Add more MR sensors as needed...


def _register_ms_entities():
    """Register MS (Switch) sensor entities."""

    # MS device sensors
    @EntityFactory.register(DeviceType.MS, MetricType.PORT_COUNT)
    def create_ms_port_count(coordinator, device, config_entry_id, network_hub=None):
        from ..devices.ms import MerakiMSDeviceSensor
        from ..sensor import MS_DEVICE_SENSOR_DESCRIPTIONS
        return MerakiMSDeviceSensor(
            device,
            coordinator,
            MS_DEVICE_SENSOR_DESCRIPTIONS["port_count"],
            config_entry_id,
            network_hub
        )

    @EntityFactory.register(DeviceType.MS, MetricType.MEMORY_USAGE)
    def create_ms_memory_usage(coordinator, device, config_entry_id, network_hub=None):
        from ..devices.ms import MerakiMSDeviceSensor
        from ..sensor import MS_DEVICE_SENSOR_DESCRIPTIONS
        return MerakiMSDeviceSensor(
            device,
            coordinator,
            MS_DEVICE_SENSOR_DESCRIPTIONS["memoryUsage"],
            config_entry_id,
            network_hub
        )

    # Add more MS sensors as needed...


def _register_organization_entities():
    """Register organization-level entities.

    Note: These don't follow the device type pattern as they're hub-level entities.
    """
    # Organization entities use the old pattern since they're not device-based
    EntityFactory._registry["api_calls"] = lambda hub, description, entry_id: _create_org_entity("MerakiHubApiCallsSensor", hub, description, entry_id)
    EntityFactory._registry["failed_api_calls"] = lambda hub, description, entry_id: _create_org_entity("MerakiHubFailedApiCallsSensor", hub, description, entry_id)
    EntityFactory._registry["device_count"] = lambda hub, description, entry_id: _create_org_entity("MerakiHubDeviceCountSensor", hub, description, entry_id)
    EntityFactory._registry["network_count"] = lambda hub, description, entry_id: _create_org_entity("MerakiHubNetworkCountSensor", hub, description, entry_id)
    EntityFactory._registry["offline_devices"] = lambda hub, description, entry_id: _create_org_entity("MerakiHubOfflineDevicesSensor", hub, description, entry_id)
    EntityFactory._registry["alerts_count"] = lambda hub, description, entry_id: _create_org_entity("MerakiHubAlertsCountSensor", hub, description, entry_id)
    EntityFactory._registry["license_expiring"] = lambda hub, description, entry_id: _create_org_entity("MerakiHubLicenseExpiringSensor", hub, description, entry_id)
    EntityFactory._registry["clients_total_count"] = lambda hub, description, entry_id: _create_org_entity("MerakiHubClientsTotalCountSensor", hub, description, entry_id)
    EntityFactory._registry["clients_usage_overall_total"] = lambda hub, description, entry_id: _create_org_entity("MerakiHubClientsUsageOverallTotalSensor", hub, description, entry_id)
    EntityFactory._registry["clients_usage_overall_downstream"] = lambda hub, description, entry_id: _create_org_entity("MerakiHubClientsUsageOverallDownstreamSensor", hub, description, entry_id)
    EntityFactory._registry["clients_usage_overall_upstream"] = lambda hub, description, entry_id: _create_org_entity("MerakiHubClientsUsageOverallUpstreamSensor", hub, description, entry_id)
    EntityFactory._registry["clients_usage_average_total"] = lambda hub, description, entry_id: _create_org_entity("MerakiHubClientsUsageAverageTotalSensor", hub, description, entry_id)
    EntityFactory._registry["bluetooth_clients_total_count"] = lambda hub, description, entry_id: _create_org_entity("MerakiHubBluetoothClientsTotalCountSensor", hub, description, entry_id)
    EntityFactory._registry["network_device_count"] = lambda hub, description, entry_id: _create_org_entity("MerakiNetworkDeviceCountSensor", hub, description, entry_id)

    # Also register the legacy entity types for backward compatibility
    EntityFactory._registry["mt_sensor"] = lambda coordinator, device, description, entry_id, network_hub: _create_device_entity("MerakiMTSensor", coordinator, device, description, entry_id, network_hub)
    EntityFactory._registry["mt_energy_sensor"] = lambda coordinator, device, description, entry_id, network_hub, power_sensor_key: _create_device_entity("MerakiMTEnergySensor", coordinator, device, description, entry_id, network_hub, power_sensor_key)
    EntityFactory._registry["mr_sensor"] = lambda coordinator, device, description, entry_id, network_hub: _create_mr_sensor(coordinator, description, entry_id)
    EntityFactory._registry["mr_device_sensor"] = lambda coordinator, device, description, entry_id, network_hub: _create_mr_device_sensor(device, coordinator, description, entry_id, network_hub)
    EntityFactory._registry["ms_sensor"] = lambda coordinator, device, description, entry_id, network_hub: _create_ms_sensor(coordinator, description, entry_id)
    EntityFactory._registry["ms_device_sensor"] = lambda coordinator, device, description, entry_id, network_hub: _create_ms_device_sensor(device, coordinator, description, entry_id, network_hub)


def _create_org_entity(class_name: str, hub: Any, description: Any, entry_id: str) -> Entity:
    """Helper to create organization entities with lazy imports."""
    from ..devices import organization
    return getattr(organization, class_name)(hub, description, entry_id)


def _create_device_entity(class_name: str, coordinator: Any, device: Any, description: Any, entry_id: str, network_hub: Any, power_sensor_key: str | None = None) -> Entity:
    """Helper to create device entities with lazy imports."""
    from ..devices import mt
    entity_class = getattr(mt, class_name)
    if power_sensor_key is not None:
        return entity_class(coordinator, device, description, entry_id, network_hub, power_sensor_key)
    return entity_class(coordinator, device, description, entry_id, network_hub)


def _create_mr_sensor(coordinator: Any, description: Any, entry_id: str) -> Entity:
    """Helper to create MR network sensor."""
    from ..devices.mr import MerakiMRSensor
    return MerakiMRSensor(coordinator, description, entry_id)


def _create_mr_device_sensor(device: Any, coordinator: Any, description: Any, entry_id: str, network_hub: Any) -> Entity:
    """Helper to create MR device sensor."""
    from ..devices.mr import MerakiMRDeviceSensor
    return MerakiMRDeviceSensor(device, coordinator, description, entry_id, network_hub)


def _create_ms_sensor(coordinator: Any, description: Any, entry_id: str) -> Entity:
    """Helper to create MS network sensor."""
    from ..devices.ms import MerakiMSSensor
    return MerakiMSSensor(coordinator, description, entry_id)


def _create_ms_device_sensor(device: Any, coordinator: Any, description: Any, entry_id: str, network_hub: Any) -> Entity:
    """Helper to create MS device sensor."""
    from ..devices.ms import MerakiMSDeviceSensor
    return MerakiMSDeviceSensor(device, coordinator, description, entry_id, network_hub)


# Register all entity types when module is imported
_register_mt_entities()
_register_mr_entities()
_register_ms_entities()
_register_organization_entities()


# Backward compatibility functions
def create_organization_entity(
    entity_type: str,
    hub: Any,
    description: SensorEntityDescription,
    entry_id: str,
) -> SensorEntity:
    """Create an organization-level entity (backward compatibility)."""
    # Organization entities don't follow the device type pattern
    # Keep using the old registry pattern for these
    if entity_type not in EntityFactory._registry:
        raise ValueError(f"Unknown organization entity type: {entity_type}")
    return cast(SensorEntity, EntityFactory._registry[entity_type](hub, description, entry_id))


def create_device_entity(
    entity_type: str,
    coordinator: MerakiSensorCoordinator,
    device: dict[str, Any],
    description: SensorEntityDescription,
    entry_id: str,
    network_hub: Any,
    **kwargs,
) -> SensorEntity:
    """Create a device-level entity (backward compatibility)."""
    # Map old entity types to new pattern
    if entity_type == "mt_sensor":
        # Determine metric type from description key
        metric_type = MetricType(description.key)
        return cast(SensorEntity, EntityFactory.create_entity(
            DeviceType.MT,
            metric_type,
            coordinator,
            device,
            entry_id,
            network_hub
        ))
    elif entity_type == "mr_device_sensor":
        metric_type = MetricType(description.key)
        return cast(SensorEntity, EntityFactory.create_entity(
            DeviceType.MR,
            metric_type,
            coordinator,
            device,
            entry_id,
            network_hub
        ))
    elif entity_type == "ms_device_sensor":
        metric_type = MetricType(description.key)
        return cast(SensorEntity, EntityFactory.create_entity(
            DeviceType.MS,
            metric_type,
            coordinator,
            device,
            entry_id,
            network_hub
        ))
    else:
        # Fall back to old registry
        if entity_type not in EntityFactory._registry:
            raise ValueError(f"Unknown device entity type: {entity_type}")
        return cast(SensorEntity, EntityFactory._registry[entity_type](
            coordinator, device, description, entry_id, network_hub, **kwargs
        ))


def create_network_entity(
    entity_type: str,
    network_hub: Any,
    description: SensorEntityDescription,
    entry_id: str,
) -> SensorEntity:
    """Create a network-level entity (backward compatibility)."""
    # Network entities use old registry pattern
    if entity_type not in EntityFactory._registry:
        raise ValueError(f"Unknown network entity type: {entity_type}")
    return cast(SensorEntity, EntityFactory._registry[entity_type](network_hub, description, entry_id))


# New pattern-based creation functions
def create_entities_for_device(
    coordinator: MerakiSensorCoordinator,
    device: dict[str, Any],
    config_entry_id: str,
    network_hub: Any = None,
) -> list[Entity]:
    """Create all applicable entities for a device using the new pattern."""
    return EntityFactory.create_entities(
        coordinator,
        device,
        config_entry_id
    )
