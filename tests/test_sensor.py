"""Test Duolingo sensors."""

from unittest.mock import MagicMock

from custom_components.duolingo.binary_sensor import DuolingualBinarySensor
from custom_components.duolingo.const import CONF_USERNAME
from custom_components.duolingo.sensor import DuolingoStreakSensor, DuolingoXPSensor

# Test constants
TEST_STREAK_COUNT = 42
TEST_XP = 12500


def _entry(username="testuser"):
    """Return a config entry stub for one username."""
    entry = MagicMock()
    entry.data = {CONF_USERNAME: username}
    return entry


def test_binary_sensor_is_on():
    """Test binary sensor is_on when streak extended today."""
    coordinator = MagicMock()
    coordinator.data = {
        "username": "testuser",
        "streak_extended_today": True,
        "site_streak": TEST_STREAK_COUNT,
    }

    sensor = DuolingualBinarySensor(coordinator, _entry())

    assert sensor.is_on is True
    assert sensor.name == "duolingo_testuser_streak_extended"
    assert sensor.unique_id == "duolingo_testuser_streak_extended"
    assert sensor.suggested_object_id == "duolingo_testuser_streak_extended"
    assert sensor.icon == "mdi:fire"


def test_binary_sensor_is_off():
    """Test binary sensor is_on when streak not extended today."""
    coordinator = MagicMock()
    coordinator.data = {
        "username": "testuser",
        "streak_extended_today": False,
        "site_streak": TEST_STREAK_COUNT,
    }

    sensor = DuolingualBinarySensor(coordinator, _entry())

    assert sensor.is_on is False


def test_binary_sensor_attributes():
    """Test binary sensor attributes."""
    coordinator = MagicMock()
    coordinator.data = {
        "username": "testuser",
        "streak_extended_today": True,
        "site_streak": TEST_STREAK_COUNT,
    }

    sensor = DuolingualBinarySensor(coordinator, _entry())
    attrs = sensor.extra_state_attributes

    assert attrs["streak_extended_today"] is True
    assert attrs["streak_length"] == TEST_STREAK_COUNT


def test_streak_sensor_native_value():
    """Test streak sensor native value."""
    coordinator = MagicMock()
    coordinator.data = {
        "username": "testuser",
        "streak_extended_today": True,
        "site_streak": TEST_STREAK_COUNT,
    }

    sensor = DuolingoStreakSensor(coordinator, _entry())

    assert sensor.native_value == TEST_STREAK_COUNT
    assert sensor.name == "duolingo_testuser_streak"
    assert sensor.unique_id == "duolingo_testuser_streak"
    assert sensor.suggested_object_id == "duolingo_testuser_streak"
    assert sensor.native_unit_of_measurement == "days"
    assert sensor.icon == "mdi:calendar"


def test_streak_sensor_no_streak():
    """Test streak sensor with no streak."""
    coordinator = MagicMock()
    coordinator.data = {
        "username": "testuser",
        "streak_extended_today": False,
        "site_streak": 0,
    }

    sensor = DuolingoStreakSensor(coordinator, _entry())

    assert sensor.native_value == 0


def test_streak_sensor_attributes():
    """Test streak sensor attributes."""
    coordinator = MagicMock()
    coordinator.data = {
        "username": "testuser",
        "streak_extended_today": True,
        "site_streak": TEST_STREAK_COUNT,
    }

    sensor = DuolingoStreakSensor(coordinator, _entry())
    attrs = sensor.extra_state_attributes

    assert attrs["username"] == "testuser"
    assert attrs["streak_extended_today"] is True
    assert "Data provided by Duolingo" in attrs.values()


def test_xp_sensor_native_value():
    """Test XP sensor native value."""
    coordinator = MagicMock()
    coordinator.data = {
        "username": "testuser",
        "streak_extended_today": True,
        "site_streak": TEST_STREAK_COUNT,
        "total_xp": TEST_XP,
    }

    sensor = DuolingoXPSensor(coordinator, _entry())

    assert sensor.native_value == TEST_XP
    assert sensor.name == "duolingo_testuser_xp"
    assert sensor.unique_id == "duolingo_testuser_xp"
    assert sensor.suggested_object_id == "duolingo_testuser_xp"
    assert sensor.native_unit_of_measurement == "XP"
    assert sensor.icon == "mdi:star"


def test_xp_sensor_no_xp():
    """Test XP sensor with no XP."""
    coordinator = MagicMock()
    coordinator.data = {
        "username": "testuser",
        "streak_extended_today": False,
        "site_streak": 0,
        "total_xp": 0,
    }

    sensor = DuolingoXPSensor(coordinator, _entry())

    assert sensor.native_value == 0


def test_xp_sensor_attributes():
    """Test XP sensor attributes."""
    coordinator = MagicMock()
    coordinator.data = {
        "username": "testuser",
        "streak_extended_today": True,
        "site_streak": TEST_STREAK_COUNT,
        "total_xp": TEST_XP,
    }

    sensor = DuolingoXPSensor(coordinator, _entry())
    attrs = sensor.extra_state_attributes

    assert attrs["username"] == "testuser"
    assert "Data provided by Duolingo" in attrs.values()


def test_username_slug_in_entity_id():
    """Usernames with punctuation become a single object id."""
    coordinator = MagicMock()
    coordinator.data = {"username": "Some.User", "site_streak": 1, "total_xp": 1}

    sensor = DuolingoStreakSensor(coordinator, _entry("Some.User"))

    assert sensor.suggested_object_id == "duolingo_some_user_streak"
