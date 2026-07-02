"""
Temperature sensor registry.

Purpose
-------
Register every available temperature sensor backend.

Why this exists
---------------
The application should never instantiate a concrete temperature
sensor directly.

Instead, the configured backend is selected through this registry.

Examples
--------
Development:
    mock

Deployment:
    raspberry_pi
"""

from room_access.hardware.temperature_sensor import (
    MockTemperatureSensor,
    RaspberryPiTemperatureSensor,
)


TEMPERATURE_SENSOR_REGISTRY = {
    # Development backend
    "mock": MockTemperatureSensor,

    # Raspberry Pi hardware backend
    "raspberry_pi": RaspberryPiTemperatureSensor,
}