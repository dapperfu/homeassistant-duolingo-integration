"""Test Duolingo API."""

from unittest.mock import MagicMock, patch

import duolingo
import pytest

from custom_components.duolingo.api import DuolingoApiClient

PASSWORD = "test-password"  # noqa: S105
DISTINCT_ID = "distinct-id"


def _client_mock(streak_payload, user_info, streak_info):
    client = MagicMock()
    client.get_user_info.return_value = user_info
    client.get_streak_info.return_value = streak_info
    client.get_streak_data.return_value = streak_payload
    return client


def test_api_get_streak_data_success():
    """Test successful API call."""
    client_mock = _client_mock(
        {
            "streakData": {
                "currentStreak": {
                    "endDate": "2023-12-01",
                    "lastExtendedDate": "2023-12-01",
                    "length": 42,
                }
            }
        },
        {"username": "testuser", "total_xp": 12500},
        {"site_streak": 42, "streak_extended_today": False},
    )

    with (
        patch(
            "custom_components.duolingo.api.duolingo.Duolingo",
            return_value=client_mock,
        ) as mock_duo,
        patch("custom_components.duolingo.api.datetime") as mock_datetime,
    ):
        mock_datetime.now.return_value.strftime.return_value = "2023-12-01"

        client = DuolingoApiClient("testuser", PASSWORD, "UTC", DISTINCT_ID)
        result = client.get_streak_data()

    mock_duo.assert_called_once_with("testuser", PASSWORD, distinct_id=DISTINCT_ID)
    assert result == {
        "username": "testuser",
        "streak_extended_today": True,
        "site_streak": 42,
        "total_xp": 12500,
    }


def test_api_get_streak_data_no_streak():
    """Test API call with no current streak."""
    client_mock = _client_mock(
        {"streakData": {"currentStreak": None}},
        {"username": "testuser", "total_xp": 0},
        {"site_streak": 0, "streak_extended_today": False},
    )

    with patch(
        "custom_components.duolingo.api.duolingo.Duolingo",
        return_value=client_mock,
    ):
        client = DuolingoApiClient("testuser", PASSWORD, "UTC", DISTINCT_ID)
        result = client.get_streak_data()

    assert result == {
        "username": "testuser",
        "streak_extended_today": False,
        "site_streak": 0,
        "total_xp": 0,
    }


def test_api_login_error():
    """Test a failed login."""
    with patch(
        "custom_components.duolingo.api.duolingo.Duolingo",
        side_effect=duolingo.DuolingoException("Login failed"),
    ):
        client = DuolingoApiClient("invaliduser", PASSWORD, "UTC", DISTINCT_ID)
        with pytest.raises(duolingo.DuolingoException, match="Login failed"):
            client.get_streak_data()
