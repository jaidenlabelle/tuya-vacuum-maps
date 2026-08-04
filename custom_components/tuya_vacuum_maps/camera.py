"""Home Assistant entity to display the map from a vacuum."""

import io
import logging
from datetime import timedelta
from typing import Any, Coroutine

import tuya_vacuum
from homeassistant.components.camera import Camera, ENTITY_ID_FORMAT
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import generate_entity_id

SCAN_INTERVAL = timedelta(seconds=10)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add camera for passed config_entry in HA."""

    _LOGGER.debug("Async setup entry")
    name = config_entry.title
    entity_id = generate_entity_id(ENTITY_ID_FORMAT, name, hass=hass)
    origin = config_entry.data["server"]
    client_id = config_entry.data["client_id"]
    client_secret = config_entry.data["client_secret"]
    device_id = config_entry.data["device_id"]

    _LOGGER.debug("Adding entities")

    # Add entity to HA.
    async_add_entities(
        [VacuumMapCamera(origin, client_id, client_secret, device_id, entity_id, hass)]
    )

    _LOGGER.debug("Done")


class VacuumMapCamera(Camera):
    """Home Assistant entity to display the map from a vacuum."""

    def __init__(self, origin, client_id, client_secret, device_id, entity_id, hass):
        """Initialize the camera."""
        super().__init__()
        self._origin = origin
        self._client_id = client_id
        self._client_secret = client_secret
        self._device_id = device_id
        self._image = None
        self.hass = hass

        # Try to get this to work
        self.content_type = "image/png"
        self.entity_id = entity_id
        self._attr_is_streaming = True

    # async def async_added_to_hass(self) -> None:
    #     self.async_schedule_update_ha_state(True)

    def update(self) -> None:
        """Update the image."""
        raise NotImplementedError

    async def async_update(self) -> None:
        """Update the image."""

        _LOGGER.debug("Updating image")

        vacuum = await self.hass.async_add_executor_job(
            tuya_vacuum.Vacuum,
            self._origin,
            self._client_id,
            self._client_secret,
            self._device_id,
        )

        # Fetch the realtime map
        vacuum_map = await self.hass.async_add_executor_job(vacuum.fetch_map)

        # Get the image
        image = vacuum_map.to_image()

        # Convert the image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="PNG")
        self._image = img_byte_arr.getvalue()

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> Coroutine[Any, Any, bytes | None]:
        """Return bytes of the image."""
        return self._image

    @property
    def should_poll(self) -> bool:
        return True
