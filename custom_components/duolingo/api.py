"""Bridge from Home Assistant to the Duolingo Python API."""

from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

import duolingo


class DuolingoApiClient:
    """Read streak and XP for one Duolingo account."""

    def __init__(
        self,
        username: str,
        password: str,
        timezone: str,
        distinct_id: str,
    ) -> None:
        """Store the account credentials used to construct the API client."""
        self._username = username
        self._password = password
        self._timezone = timezone
        self._distinct_id = distinct_id

    def get_streak_data(self) -> dict[str, Any]:
        """Log in and return the sensor payload for this account."""
        client = duolingo.Duolingo(
            self._username,
            self._password,
            distinct_id=self._distinct_id,
        )
        user_info = client.get_user_info()
        streak_info = client.get_streak_info()
        streak_payload = client.get_streak_data()
        current = _current_streak(streak_payload)
        site_streak = streak_info.get("site_streak")
        if site_streak is None:
            site_streak = current.get("length") or 0

        return {
            "username": user_info.get("username") or self._username,
            "streak_extended_today": self._extended_today(
                current.get("lastExtendedDate")
            ),
            "site_streak": site_streak or 0,
            "total_xp": user_info.get("total_xp") or 0,
        }

    def _extended_today(self, last_extended: Any) -> bool:
        """Return whether the streak was extended on today's Home Assistant date."""
        if not isinstance(last_extended, str) or len(last_extended) < 10:  # noqa: PLR2004
            return False
        today = datetime.now(ZoneInfo(self._timezone)).strftime("%Y-%m-%d")
        return last_extended[:10] == today


def _current_streak(payload: Any) -> dict[str, Any]:
    """Return the currentStreak object from a streak payload."""
    if not isinstance(payload, dict):
        return {}
    streak_data = payload.get("streakData") or {}
    if not isinstance(streak_data, dict):
        return {}
    current = streak_data.get("currentStreak") or {}
    if not isinstance(current, dict):
        return {}
    return current
