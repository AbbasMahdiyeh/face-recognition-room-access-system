"""
Hardware registry.

Purpose
-------
Provide a single place where hardware implementations
are registered.

Why this exists
---------------
The application should remain independent from concrete
hardware implementations.

As new hardware controllers are introduced, they can be
registered here without increasing the complexity of the
factory.

Architecture
------------
Settings
    ↓
HardwareFactory
    ↓
HardwareRegistry
    ↓
Concrete Hardware Controller
"""

from room_access.hardware.led_controller import MockLEDController

HARDWARE_REGISTRY = {
    "mock": MockLEDController,
}