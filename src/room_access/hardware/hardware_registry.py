"""
Hardware registry.

Purpose
-------
Register available hardware controller implementations.

Why this exists
---------------
The application should not directly depend on concrete hardware
controllers.

During laptop development, the system uses mock hardware.
During Raspberry Pi deployment, the backend can be switched to
real GPIO hardware through configuration.
"""

from room_access.hardware.led_controller import MockLEDController
from room_access.hardware.raspberry_pi_led_controller import RaspberryPiLEDController


HARDWARE_REGISTRY = {
    # Development backend
    "mock": MockLEDController,

    # Raspberry Pi GPIO backend
    "raspberry_pi": RaspberryPiLEDController,
}