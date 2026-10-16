"""DuolingoEntity class."""

import re

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import CONF_USERNAME, DOMAIN


def username_slug(username: str) -> str:
    """Return an entity-id fragment for a Duolingo username."""
    slug = re.sub(r"[^a-z0-9]+", "_", username.lower()).strip("_")
    return slug or "user"


class DuolingoEntity(CoordinatorEntity):
    """Base entity for Duolingual integration."""

    _sensor_key: str

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self.config_entry = config_entry
        username = config_entry.data[CONF_USERNAME]
        self._object_id = f"{DOMAIN}_{username_slug(username)}_{self._sensor_key}"

    @property
    def name(self) -> str:
        """Return the entity name used to build the entity id."""
        return self._object_id

    @property
    def unique_id(self) -> str:
        """Return a unique ID to use for this entity."""
        return self._object_id

    @property
    def suggested_object_id(self) -> str:
        """Return the object id Home Assistant uses for the entity id."""
        return self._object_id

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device for this Duolingo account."""
        username = self.config_entry.data[CONF_USERNAME]
        return DeviceInfo(
            identifiers={(DOMAIN, username.lower())},
            manufacturer="Duolingo",
            name=f"Duolingo {username}",
        )
