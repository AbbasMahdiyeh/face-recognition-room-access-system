"""
System health check.

This module verifies whether the project runtime environment
is ready before starting the live access-control application.
"""

from pathlib import Path

from room_access.config.settings import Settings

import platform


class HealthCheck:
    """
    Check important project folders, settings, and hardware configuration.
    """

    def __init__(self):
        self.settings = Settings()

    def run(self) -> dict:
        """
        Run all health checks and return the results.
        """

        results = {}

        results["config/settings.json"] = Path("config/settings.json").exists()
        results["authorized_faces"] = Path("data/authorized_faces").exists()
        results["embeddings"] = Path("data/embeddings").exists()
        results["logs"] = Path("data/logs").exists()
        results["events"] = Path("data/events").exists()

        results["camera_backend"] = self.settings.get(
            "camera",
            "backend",
            "unknown",
        )

        results["led_backend"] = self.settings.get(
            "hardware",
            "led_backend",
            "unknown",
        )

        results["temperature_backend"] = self.settings.get(
            "hardware",
            "temperature_backend",
            "unknown",
        )

        results["platform"] = platform.system()
        results["machine"] = platform.machine()

        results["is_raspberry_pi"] = Path(
            "/proc/device-tree/model"
            ).exists()

        return results