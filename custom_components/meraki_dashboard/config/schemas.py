"""Configuration validation schemas for Meraki Dashboard integration."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, ClassVar

from ..const import (
    DEFAULT_BASE_URL,
    DEFAULT_DISCOVERY_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DYNAMIC_DATA_REFRESH_INTERVAL_MINUTES,
    REGIONAL_BASE_URLS,
    SEMI_STATIC_DATA_REFRESH_INTERVAL_MINUTES,
    STATIC_DATA_REFRESH_INTERVAL_MINUTES,
)
from ..exceptions import ConfigurationError


@dataclass
class IntervalConfig:
    """Configuration for interval validation."""

    value: int
    min_seconds: int = 60
    max_seconds: int = 86400

    def __post_init__(self) -> None:
        """Validate interval after initialization."""
        if not isinstance(self.value, int):
            raise ConfigurationError(
                f"Interval must be an integer, got {type(self.value).__name__}"
            )

        if self.value < self.min_seconds:
            raise ConfigurationError(
                f"Interval must be at least {self.min_seconds} seconds, got {self.value}"
            )

        if self.value > self.max_seconds:
            raise ConfigurationError(
                f"Interval must be at most {self.max_seconds} seconds, got {self.value}"
            )


@dataclass
class APIKeyConfig:
    """Configuration for API key validation."""

    value: str
    # Meraki API keys are typically 40 characters long
    MERAKI_API_KEY_PATTERN: ClassVar[re.Pattern] = re.compile(r"^[a-fA-F0-9]{40}$")

    def __post_init__(self) -> None:
        """Validate API key after initialization."""
        if not isinstance(self.value, str):
            raise ConfigurationError("API key must be a string")

        if not self.value.strip():
            raise ConfigurationError("API key cannot be empty")

        # Basic format validation - Meraki API keys are typically 40 hex characters
        if len(self.value) != 40:
            raise ConfigurationError(
                f"API key must be 40 characters long, got {len(self.value)}"
            )

        if not self.MERAKI_API_KEY_PATTERN.match(self.value):
            raise ConfigurationError(
                "API key must contain only hexadecimal characters (0-9, a-f, A-F)"
            )


@dataclass
class BaseURLConfig:
    """Configuration for base URL validation."""

    value: str
    allowed_urls: list[str] = field(
        default_factory=lambda: list(REGIONAL_BASE_URLS.values())
    )

    def __post_init__(self) -> None:
        """Validate base URL after initialization."""
        if not isinstance(self.value, str):
            raise ConfigurationError("Base URL must be a string")

        if not self.value.strip():
            raise ConfigurationError("Base URL cannot be empty")

        # Must be HTTPS
        if not self.value.startswith("https://"):
            raise ConfigurationError("Base URL must use HTTPS")

        # Should be one of the allowed URLs
        if self.value not in self.allowed_urls:
            raise ConfigurationError(
                f"Base URL must be one of: {', '.join(self.allowed_urls)}"
            )


@dataclass
class OrganizationIDConfig:
    """Configuration for organization ID validation."""

    value: str
    # Meraki organization IDs can contain letters, numbers, and hyphens
    ORG_ID_PATTERN: ClassVar[re.Pattern] = re.compile(r"^[a-zA-Z0-9\-]+$")

    def __post_init__(self) -> None:
        """Validate organization ID after initialization."""
        if not isinstance(self.value, str):
            raise ConfigurationError("Organization ID must be a string")

        if not self.value.strip():
            raise ConfigurationError("Organization ID cannot be empty")

        if not self.ORG_ID_PATTERN.match(self.value):
            raise ConfigurationError(
                "Organization ID must contain only letters, numbers, and hyphens"
            )


@dataclass
class DeviceSerialConfig:
    """Configuration for device serial validation."""

    value: str
    # Meraki device serials follow a specific pattern
    SERIAL_PATTERN: ClassVar[re.Pattern] = re.compile(r"^[A-Z0-9\-]+$")

    def __post_init__(self) -> None:
        """Validate device serial after initialization."""
        if not isinstance(self.value, str):
            raise ConfigurationError("Device serial must be a string")

        if not self.value.strip():
            raise ConfigurationError("Device serial cannot be empty")

        if not self.SERIAL_PATTERN.match(self.value):
            raise ConfigurationError(
                "Device serial must contain only uppercase letters, digits, and hyphens"
            )


@dataclass
class TieredRefreshConfig:
    """Configuration for tiered refresh intervals."""

    static_interval: int
    semi_static_interval: int
    dynamic_interval: int

    def __post_init__(self) -> None:
        """Validate tiered refresh intervals after initialization."""
        # Validate individual intervals
        IntervalConfig(self.static_interval, min_seconds=3600, max_seconds=86400)
        IntervalConfig(self.semi_static_interval, min_seconds=1800, max_seconds=43200)
        IntervalConfig(self.dynamic_interval, min_seconds=300, max_seconds=7200)

        # Validate relationship: dynamic < semi_static < static
        if self.dynamic_interval >= self.semi_static_interval:
            raise ConfigurationError(
                f"Dynamic interval ({self.dynamic_interval}s) must be less than "
                f"semi-static interval ({self.semi_static_interval}s)"
            )

        if self.semi_static_interval >= self.static_interval:
            raise ConfigurationError(
                f"Semi-static interval ({self.semi_static_interval}s) must be less than "
                f"static interval ({self.static_interval}s)"
            )


@dataclass
class HubIntervalConfig:
    """Configuration for hub-specific intervals."""

    hub_id: str
    scan_interval: int | None = None
    discovery_interval: int | None = None
    auto_discovery: bool | None = None

    def __post_init__(self) -> None:
        """Validate hub-specific intervals after initialization."""
        if not isinstance(self.hub_id, str) or not self.hub_id.strip():
            raise ConfigurationError("Hub ID must be a non-empty string")

        if self.scan_interval is not None:
            IntervalConfig(self.scan_interval, min_seconds=60, max_seconds=3600)

        if self.discovery_interval is not None:
            IntervalConfig(self.discovery_interval, min_seconds=300, max_seconds=86400)

        if self.auto_discovery is not None and not isinstance(
            self.auto_discovery, bool
        ):
            raise ConfigurationError("Auto discovery must be a boolean")


@dataclass
class MerakiConfigSchema:
    """Complete configuration schema for Meraki Dashboard integration."""

    # Core configuration (stored in data)
    api_key: str
    base_url: str = DEFAULT_BASE_URL
    organization_id: str = ""

    # Options configuration
    scan_interval: int = DEFAULT_SCAN_INTERVAL
    auto_discovery: bool = True
    discovery_interval: int = DEFAULT_DISCOVERY_INTERVAL
    selected_devices: list[str] = field(default_factory=list)

    # Hub-specific configuration
    hub_scan_intervals: dict[str, int] = field(default_factory=dict)
    hub_discovery_intervals: dict[str, int] = field(default_factory=dict)
    hub_auto_discovery: dict[str, bool] = field(default_factory=dict)

    # Tiered refresh intervals
    static_data_interval: int = STATIC_DATA_REFRESH_INTERVAL_MINUTES * 60
    semi_static_data_interval: int = SEMI_STATIC_DATA_REFRESH_INTERVAL_MINUTES * 60
    dynamic_data_interval: int = DYNAMIC_DATA_REFRESH_INTERVAL_MINUTES * 60

    def __post_init__(self) -> None:
        """Validate complete configuration after initialization."""
        # Validate core configuration
        APIKeyConfig(self.api_key)
        BaseURLConfig(self.base_url)
        if self.organization_id:  # Only validate if provided
            OrganizationIDConfig(self.organization_id)

        # Validate global intervals
        IntervalConfig(self.scan_interval, min_seconds=60, max_seconds=3600)
        IntervalConfig(self.discovery_interval, min_seconds=300, max_seconds=86400)

        # Validate auto discovery
        if not isinstance(self.auto_discovery, bool):
            raise ConfigurationError("Auto discovery must be a boolean")

        # Validate selected devices
        if not isinstance(self.selected_devices, list):
            raise ConfigurationError("Selected devices must be a list")

        for serial in self.selected_devices:
            DeviceSerialConfig(serial)

        # Validate hub-specific configurations
        for hub_id, interval in self.hub_scan_intervals.items():
            HubIntervalConfig(hub_id, scan_interval=interval)

        for hub_id, interval in self.hub_discovery_intervals.items():
            HubIntervalConfig(hub_id, discovery_interval=interval)

        for hub_id, enabled in self.hub_auto_discovery.items():
            HubIntervalConfig(hub_id, auto_discovery=enabled)

        # Validate tiered refresh intervals
        TieredRefreshConfig(
            static_interval=self.static_data_interval,
            semi_static_interval=self.semi_static_data_interval,
            dynamic_interval=self.dynamic_data_interval,
        )

    @classmethod
    def from_config_entry(
        cls, data: dict[str, Any], options: dict[str, Any] | None = None
    ) -> MerakiConfigSchema:
        """Create schema from config entry data and options.

        Args:
            data: Config entry data
            options: Config entry options

        Returns:
            Validated configuration schema
        """
        options = options or {}

        return cls(
            # Core configuration from data
            api_key=data["api_key"],
            base_url=data.get("base_url", DEFAULT_BASE_URL),
            organization_id=data.get("organization_id", ""),
            # Options configuration
            scan_interval=options.get("scan_interval", DEFAULT_SCAN_INTERVAL),
            auto_discovery=options.get("auto_discovery", True),
            discovery_interval=options.get(
                "discovery_interval", DEFAULT_DISCOVERY_INTERVAL
            ),
            selected_devices=options.get("selected_devices", []),
            # Hub-specific configuration
            hub_scan_intervals=options.get("hub_scan_intervals", {}),
            hub_discovery_intervals=options.get("hub_discovery_intervals", {}),
            hub_auto_discovery=options.get("hub_auto_discovery", {}),
            # Tiered refresh intervals
            static_data_interval=options.get(
                "static_data_interval", STATIC_DATA_REFRESH_INTERVAL_MINUTES * 60
            ),
            semi_static_data_interval=options.get(
                "semi_static_data_interval",
                SEMI_STATIC_DATA_REFRESH_INTERVAL_MINUTES * 60,
            ),
            dynamic_data_interval=options.get(
                "dynamic_data_interval", DYNAMIC_DATA_REFRESH_INTERVAL_MINUTES * 60
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert schema to dictionary for storage.

        Returns:
            Dictionary representation of the configuration
        """
        return {
            "api_key": self.api_key,
            "base_url": self.base_url,
            "organization_id": self.organization_id,
            "scan_interval": self.scan_interval,
            "auto_discovery": self.auto_discovery,
            "discovery_interval": self.discovery_interval,
            "selected_devices": self.selected_devices,
            "hub_scan_intervals": self.hub_scan_intervals,
            "hub_discovery_intervals": self.hub_discovery_intervals,
            "hub_auto_discovery": self.hub_auto_discovery,
            "static_data_interval": self.static_data_interval,
            "semi_static_data_interval": self.semi_static_data_interval,
            "dynamic_data_interval": self.dynamic_data_interval,
        }


def validate_config_migration(
    old_config: dict[str, Any], new_config: dict[str, Any]
) -> bool:
    """Validate configuration migration from old to new format.

    Args:
        old_config: Previous configuration
        new_config: New configuration to validate

    Returns:
        True if migration is valid

    Raises:
        ConfigurationError: If migration is invalid
    """
    # Ensure API key hasn't changed (security measure)
    if old_config.get("api_key") != new_config.get("api_key"):
        raise ConfigurationError("API key cannot be changed during migration")

    # Ensure organization ID hasn't changed
    if old_config.get("organization_id") != new_config.get("organization_id"):
        raise ConfigurationError("Organization ID cannot be changed during migration")

    # Validate the new configuration
    try:
        MerakiConfigSchema.from_config_entry(
            data={
                k: v
                for k, v in new_config.items()
                if k in ["api_key", "base_url", "organization_id"]
            },
            options={
                k: v
                for k, v in new_config.items()
                if k not in ["api_key", "base_url", "organization_id"]
            },
        )
    except Exception as e:
        raise ConfigurationError(f"Invalid configuration after migration: {e}") from e

    return True
