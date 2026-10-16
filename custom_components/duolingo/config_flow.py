"""Adds config flow for Duolingual."""

from typing import Any
from uuid import uuid4

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.selector import (
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)

from .api import DuolingoApiClient
from .const import (
    CONF_DISTINCT_ID,
    CONF_PASSWORD,
    CONF_USERNAME,
    DOMAIN,
)


class DuolingualFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Duolingual."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self) -> None:
        """Initialize."""
        self._errors: dict[str, str] = {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            username = user_input[CONF_USERNAME]
            password = user_input[CONF_PASSWORD]
            await self.async_set_unique_id(username.lower())
            self._abort_if_unique_id_configured()

            distinct_id = str(uuid4())
            try:
                valid = await self._test_credentials(username, password, distinct_id)
            except Exception:  # noqa: BLE001
                valid = False
            if valid:
                return self.async_create_entry(
                    title=username,
                    data={
                        CONF_USERNAME: username,
                        CONF_PASSWORD: password,
                        CONF_DISTINCT_ID: distinct_id,
                    },
                )
            self._errors["base"] = "auth"
            return await self._show_config_form(user_input)

        return await self._show_config_form({CONF_USERNAME: ""})

    async def _show_config_form(self, user_input: dict[str, Any]) -> FlowResult:
        """Show the username and password form."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_USERNAME, default=user_input.get(CONF_USERNAME, "")
                    ): TextSelector(),
                    vol.Required(CONF_PASSWORD): TextSelector(
                        TextSelectorConfig(type=TextSelectorType.PASSWORD)
                    ),
                }
            ),
            errors=self._errors,
        )

    async def _test_credentials(
        self, username: str, password: str, distinct_id: str
    ) -> bool:
        """Return true if the username and password can log in."""
        try:
            client = DuolingoApiClient(
                username,
                password,
                self.hass.config.time_zone,
                distinct_id,
            )
            await self.hass.async_add_executor_job(client.get_streak_data)
        except Exception:  # noqa: BLE001
            return False
        else:
            return True
