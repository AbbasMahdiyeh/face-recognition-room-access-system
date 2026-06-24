"""
Application settings loader.

This module loads project configuration from config/settings.json.
Centralizing settings keeps important runtime parameters out of
application logic and makes the system easier to tune.
"""

import json
from pathlib import Path


class Settings:
    """
    Load and provide access to application settings.
    """

    def __init__(self, settings_path: str = "config/settings.json"):
        self.settings_path = Path(settings_path)
        self.data = self._load_settings()

    def _load_settings(self) -> dict:
        """
        Load settings from JSON.
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