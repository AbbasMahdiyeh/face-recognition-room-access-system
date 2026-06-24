"""
Hardware factory.

Purpose
-------
Create hardware controllers from application settings.

Why this exists
---------------
LiveAccessApp should not know whether the system is using mock
hardware during laptop development or real GPIO hardware on a
Raspberry Pi.

The factory reads the selected backend from settings and resolves
the concrete controller through HARDWARE_REGISTRY.

Architecture
------------
settings.json
    ↓
Settings
    ↓
HardwareFactory
    ↓
HardwareRegistry
    ↓
Concrete Hardware Controller
"""

from room_access.hardware.hardware_registry import HARDWARE_REGISTRY


class HardwareFactory:
    """
    Create hardware controllers from configuration.
    """

    @staticmethod
    def create_led_controller(settings):
        """
        Create the configured LED controller.

        Adding a new LED backend only requires registering it in
        HARDWARE_REGISTRY. The factory logic stays unchanged.
        """

        backend = settings.get(
            "hardware",
            "led_backend",
            "mock",
        )

        controller_class = HARDWARE_REGISTRY.get(backend)

        if controller_class is None:
            available_backends = ", ".join(HARDWARE_REGISTRY.keys())

            raise ValueError(
                f"Unknown LED backend: {backend}. "
                f"Available backends: {available_backends}"
            )

        return controller_class()