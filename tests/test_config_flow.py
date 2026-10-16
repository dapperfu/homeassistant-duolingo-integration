"""Test Duolingo config flow."""

from unittest.mock import patch

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.helpers.selector import TextSelector, TextSelectorType
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.duolingo.const import (
    CONF_DISTINCT_ID,
    CONF_PASSWORD,
    CONF_USERNAME,
    DOMAIN,
)

PASSWORD = "test-password"  # noqa: S105


def _schema_by_key(schema):
    """Return schema fields keyed by the field name."""
    fields = {}
    for key, value in schema.items():
        name = key.schema if hasattr(key, "schema") else key
        fields[name] = value
    return fields


async def test_form_user(hass: HomeAssistant):
    """Test user config flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {}

    fields = _schema_by_key(result["data_schema"].schema)
    assert CONF_USERNAME in fields
    assert isinstance(fields[CONF_USERNAME], TextSelector)
    assert isinstance(fields[CONF_PASSWORD], TextSelector)
    assert fields[CONF_PASSWORD].config["type"] == TextSelectorType.PASSWORD

    with patch(
        "custom_components.duolingo.config_flow.DuolingoApiClient",
    ) as mock_client:
        mock_client.return_value.get_streak_data.return_value = {
            "username": "testuser",
            "streak_extended_today": True,
            "site_streak": 42,
        }

        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_USERNAME: "testuser",
                CONF_PASSWORD: PASSWORD,
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] == FlowResultType.CREATE_ENTRY
    assert result2["title"] == "testuser"
    assert result2["data"][CONF_USERNAME] == "testuser"
    assert result2["data"][CONF_PASSWORD] == PASSWORD
    assert result2["data"][CONF_DISTINCT_ID]


async def test_form_invalid_auth(hass: HomeAssistant):
    """Test invalid authentication."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.duolingo.config_flow.DuolingoApiClient",
    ) as mock_client:
        mock_client.return_value.get_streak_data.side_effect = ValueError(
            "No user found"
        )

        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_USERNAME: "invaliduser",
                CONF_PASSWORD: PASSWORD,
            },
        )

    assert result2["type"] == FlowResultType.FORM
    assert result2["errors"]["base"] == "auth"
    fields = _schema_by_key(result2["data_schema"].schema)
    assert isinstance(fields[CONF_PASSWORD], TextSelector)
    assert fields[CONF_PASSWORD].config["type"] == TextSelectorType.PASSWORD


async def test_form_connection_error(hass: HomeAssistant):
    """Test connection error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.duolingo.config_flow.DuolingoApiClient",
    ) as mock_client:
        mock_client.return_value.get_streak_data.side_effect = Exception(
            "Connection error"
        )

        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_USERNAME: "testuser",
                CONF_PASSWORD: PASSWORD,
            },
        )

    assert result2["type"] == FlowResultType.FORM
    assert result2["errors"]["base"] == "auth"


async def test_form_already_configured(hass: HomeAssistant):
    """Test that the same username cannot be added twice."""
    MockConfigEntry(
        domain=DOMAIN,
        unique_id="testuser",
        data={
            CONF_USERNAME: "testuser",
            CONF_PASSWORD: PASSWORD,
            CONF_DISTINCT_ID: "already",
        },
    ).add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_USERNAME: "TestUser",
            CONF_PASSWORD: PASSWORD,
        },
    )

    assert result2["type"] == FlowResultType.ABORT
    assert result2["reason"] == "already_configured"
