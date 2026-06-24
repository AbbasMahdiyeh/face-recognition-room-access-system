"""
Temperature sensor abstraction.

This module provides a mock temperature sensor for development.

The application can use this class before the real Raspberry Pi
temperature sensor is connected. Later, a hardware-specific sensor
can expose the same public method and replace this mock version.
"""


class MockTemperatureSensor:
    """
    Simulate a room temperature sensor.
    """

    def __init__(
        self,
        temperature_celsius: float = 23.5,
    ):
        """
        Store a fixed mock temperature value.

        This keeps the dashboard and logger testable before the
        physical sensor is available.
        """

        self.temperature_celsius = temperature_celsius

    def read_temperature(self) -> float:
        """
        Return the current room temperature in Celsius.
        """

        return self.temperature_celsius