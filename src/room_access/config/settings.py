"""
Application settings loader.

Purpose
-------
Load the appropriate configuration profile for the current platform.

Profiles
--------
Windows:
    config/settings.laptop.json

Linux (Raspberry Pi):
    config/settings.raspberrypi.json

This allows the same project to run on both development and deployment
machines without manually editing configuration files.
"""

import json
import platform
from pathlib import Path


class Settings:
    """
    Load and provide access to application settings.
    """

    def __init__(self):
        """
        Select the appropriate settings profile automatically.
        """

        self.settings_path = self._detect_settings_profile()
        self.data = self._load_settings()

    def _detect_settings_profile(self) -> Path:
        """
        Select the configuration profile based on the operating system.
        """

        config_directory = Path("config")

        if platform.system() == "Windows":
            return config_directory / "settings.laptop.json"

        return config_directory / "settings.raspberrypi.json"

    def _load_settings(self) -> dict:
        """
        Load settings from the selected JSON profile.
        """

        with self.settings_path.open(
            mode="r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    def get(
        self,
        section: str,
        key: str,
        default=None,
    ):
        """
        Read one setting value with an optional default.
        """

        return self.data.get(
            section,
            {},
        ).get(
            key,
            default,
        )