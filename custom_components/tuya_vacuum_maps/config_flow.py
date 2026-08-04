"""Handle Home Assistant config flow for the Tuya Vacuum Maps integration."""

import logging
from typing import Any, override

import tuya_vacuum
from tuya_vacuum.errors import (
    CrossRegionAccessError,
    InvalidClientIDError,
    InvalidClientSecretError,
    InvalidDeviceIDError,
)
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import (
    CONF_CLIENT_ID,
    CONF_CLIENT_SECRET,
    CONF_DEVICE_ID,
    CONF_NAME,
)

from .const import CONF_SERVER, CONF_SERVER_WEST_AMERICA, CONF_SERVERS, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def validate_input(data: dict) -> None:
    """Validate that the user input allows us to connect."""

    vacuum = tuya_vacuum.Vacuum(
        data["server"], data["client_id"], data["client_secret"], data["device_id"]
    )

    vacuum.fetch_map()


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Tuya Vacuum Maps."""

    # Schema version of the entries it creates
    # Home Assistant will call the migrate method if the version changes
    VERSION = 1
    MINOR_VERSION = 1

    @override
    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """This is Invoked when a user initiates a flow via the user interface.

        Also called when discovered but a matching discovery step is not defined.
        """

        # List of errors related to the form
        errors = {}

        if user_input is not None:
            try:
                try:
                    await validate_input(user_input)

                    # Process the information
                    return self.async_create_entry(
                        title=user_input.pop(CONF_NAME), data=user_input
                    )
                except Exception as err:
                    _LOGGER.error("Error occurred while validating: %s", err)
                    raise err
            except CrossRegionAccessError:
                errors[CONF_SERVER] = (
                    "Cross region access is not allowed, data center mismatch."
                )
            except InvalidClientIDError:
                errors[CONF_CLIENT_ID] = "Invalid Client ID."
            except InvalidClientSecretError:
                errors[CONF_CLIENT_SECRET] = "Invalid Client Secret."
            except InvalidDeviceIDError:
                errors[CONF_DEVICE_ID] = "Invalid Device ID."
            except Exception:  # pylint: disable=broad-except
                errors["base"] = "Unknown error occurred."
        # Define the schema of the form
        data_schema = vol.Schema(
            {
                # Device Name
                vol.Required(CONF_NAME, default="Vacuum Map"): str,
                # Server API URL
                vol.Required(CONF_SERVER, default=CONF_SERVER_WEST_AMERICA): vol.In(
                    CONF_SERVERS
                ),
                # Client ID
                vol.Required(CONF_CLIENT_ID, default=""): str,
                # Client Secret
                vol.Required(CONF_CLIENT_SECRET, default=""): str,
                # Device ID
                vol.Required(CONF_DEVICE_ID, default=""): str,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
