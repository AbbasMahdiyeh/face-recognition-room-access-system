"""
Raspberry Pi camera implementation.

This module will provide live image acquisition
from the Raspberry Pi Camera Module.
"""

from .camera_interface import CameraInterface


class RaspberryPiCamera(CameraInterface):
    """
    Raspberry Pi Camera implementation.
    """

    def get_frame(self):
        raise NotImplementedError(
            "Raspberry Pi camera integration is not implemented yet."
        )