"""Test setting up more than one Duolingo account."""

from unittest.mock import MagicMock, patch

from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.duolingo.const import (
    CONF_DISTINCT_ID,
    CONF_PASSWORD,
    CONF_USERNAME,
    DOMAIN,
)

PASSWORD = "test-password"  # noqa: S105


def _fake_duolingo(username, password, *, distinct_id=None):  # noqa: ARG001
    """Return a Duolingo client stub for one username."""
    client = MagicMock()
    client.get_user_info.return_value = {"username": username, "total_xp": 10}
    client.get_streak_info.return_value = {
        "site_streak": 3,
        "streak_extended_today": False,
    }
    client.get_streak_data.return_value = {
        "streakData": {
            "currentStreak": {
                "length": 3,
                "lastExtendedDate": "2020-01-01",
            }
        }
    }
    return client


async def test_two_users_get_separate_entity_ids(hass: HomeAssistant):
    """Each account gets sensor.duolingo_<username>_<sensor>."""
    entries = []
    for username in ("alice", "bob"):
        entry = MockConfigEntry(
            domain=DOMAIN,
            unique_id=username,
            title=username,
            data={
                CONF_USERNAME: username,
                CONF_PASSWORD: PASSWORD,
                CONF_DISTINCT_ID: f"id-{username}",
            },
        )
        entry.add_to_hass(hass)
        entries.append(entry)

    with patch(
        "custom_components.duolingo.api.duolingo.Duolingo",
        side_effect=_fake_duolingo,
    ):
        assert await hass.config_entries.async_setup(entries[0].entry_id)
        await hass.async_block_till_done()

    for entry in entries:
        assert entry.state is ConfigEntryState.LOADED

    entity_ids = set(hass.states.async_entity_ids())
    assert "sensor.duolingo_alice_streak" in entity_ids
    assert "sensor.duolingo_alice_xp" in entity_ids
    assert "binary_sensor.duolingo_alice_streak_extended" in entity_ids
    assert "sensor.duolingo_bob_streak" in entity_ids
    assert "sensor.duolingo_bob_xp" in entity_ids
    assert "binary_sensor.duolingo_bob_streak_extended" in entity_ids
