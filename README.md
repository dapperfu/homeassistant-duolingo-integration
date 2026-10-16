# Duolingual - A Home Assistant integration for Duolingo

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)
[![CI][ci-shield]][ci]

_Home Assistant integration to track your Duolingo daily streak progress._

## About


This integration asks for a Duolingo username and password and creates sensors to monitor streak activity. Add it again for each additional account. Entity ids look like `sensor.duolingo_<username>_streak`.

<img width="416" alt="image" src="https://github.com/user-attachments/assets/28036aaa-67e7-419b-980e-5926433aad07" />

<img width="343" alt="image" src="https://github.com/user-attachments/assets/66d0518e-802a-4a27-8397-f1fdaa551a06" />



- **🔥 Binary Sensor**: Shows if you extended your streak today (on/off)
- **📅 Streak Sensor**: Displays your current streak count in days
- **⭐ XP Sensor**: Shows your total XP across all courses

### Fork Notes

This is a fork of [sphanley/Duolinguist](https://github.com/sphanley/Duolinguist), updated to work with current Duolingo APIs and modern Home Assistant versions.

⚠️ **Important**: This integration uses reverse-engineered Duolingo APIs since no official API documentation exists. It may break if Duolingo changes their endpoints.

## Installation

### Manual Installation

1. Download the latest release or clone this repository
2. Copy the `custom_components/duolingo/` folder to your Home Assistant `custom_components/` directory
3. Restart Home Assistant
4. Go to **Settings → Devices & Services → Add Integration** and search for "Duolingual"

### HACS Installation

Add this repository as a custom repository in HACS:

1. Go to HACS → Integrations → ⋮ → Custom repositories
2. Add repository URL: `https://github.com/TimCinel/duolingual`
3. Category: Integration
4. Install and restart Home Assistant

## Configuration

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for "Duolingual"
3. Enter the Duolingo username and password. The password field is masked.
4. Repeat those steps for each additional account
5. Each account gets its own entities, for example `sensor.duolingo_<username>_streak`, `sensor.duolingo_<username>_xp`, and `binary_sensor.duolingo_<username>_streak_extended`

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[ci-shield]: https://img.shields.io/github/actions/workflow/status/TimCinel/duolingual/ci.yml?style=for-the-badge
[ci]: https://github.com/TimCinel/duolingual/actions
[license-shield]: https://img.shields.io/github/license/TimCinel/duolingual.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/TimCinel/duolingual.svg?style=for-the-badge
[releases]: https://github.com/TimCinel/duolingual/releases
