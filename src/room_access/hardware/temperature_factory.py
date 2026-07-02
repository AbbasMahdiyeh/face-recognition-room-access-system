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

        Mock temperature uses a fixed development value.

        Raspberry Pi temperature reads from the configured OneWire
        device path so the deployment can be adjusted without
        changing application code.
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

        if backend == "raspberry_pi":
            devices_root = settings.get(
                "hardware",
                "temperature_sensor_path",
                "/sys/bus/w1/devices",
            )

            return sensor_class(
                devices_root=devices_root,
            )

        return sensor_class()