"""
Temperature sensor registry.

Purpose
-------
Register available temperature sensor implementations.

Why this exists
---------------
The application should not directly depend on a specific
temperature sensor implementation.

During laptop development, the system uses a mock sensor.
During Raspberry Pi deployment, the backend can be switched
to a real sensor through configuration.
"""

from room_access.hardware.temperature_sensor import MockTemperatureSensor


TEMPERATURE_SENSOR_REGISTRY = {
    "mock": MockTemperatureSensor,
}