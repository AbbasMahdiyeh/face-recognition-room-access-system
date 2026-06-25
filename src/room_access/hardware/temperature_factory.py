"""
Temperature sensor factory.

Purpose
-------
Create the configured temperature sensor backend.

Architecture
------------
settings.json
    ↓
Settings
    ↓
TemperatureFactory
    ↓
TemperatureRegistry
    ↓
Concrete Temperature Sensor
"""

from room_access.hardware.temperature_registry import TEMPERATURE_SENSOR_REGISTRY


class TemperatureFactory:
    """
    Create temperature sensor backends from configuration.
    """

    @staticmethod
    def create_temperature_sensor(settings):
        """
        Create the configured temperature sensor.

        New sensor backends only need to be registered in
        TEMPERATURE_SENSOR_REGISTRY.
        """

        backend = settings.get(
            "hardware",
            "temperature_backend",
            "mock",
        )

        sensor_class = TEMPERATURE_SENSOR_REGISTRY.get(backend)

        if sensor_class is None:
            available_backends = ", ".join(TEMPERATURE_SENSOR_REGISTRY.keys())

            raise ValueError(
                f"Unknown temperature backend: {backend}. "
                f"Available backends: {available_backends}"
            )

        return sensor_class()