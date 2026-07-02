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

        Mock hardware does not need GPIO pin configuration.

        Raspberry Pi hardware receives the configured BCM GPIO pins
        from settings.json so wiring can be changed without modifying
        application code.
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

        if backend == "raspberry_pi":
            green_pin = settings.get(
                "hardware",
                "green_led_pin",
                17,
            )

            red_pin = settings.get(
                "hardware",
                "red_led_pin",
                27,
            )

            return controller_class(
                green_pin=green_pin,
                red_pin=red_pin,
            )

        return controller_class()