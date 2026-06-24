"""
Raspberry Pi camera implementation.

This module provides the Raspberry Pi implementation of the
CameraInterface.

The current version is a placeholder. A future implementation
will use the Picamera2 library while preserving the same public
interface as LaptopWebcamCamera. This allows the application to
switch camera backends without changing the application logic.
"""

from .camera_interface import CameraInterface


class RaspberryPiCamera(CameraInterface):
    """
    Raspberry Pi camera implementation placeholder.
    """

    def open(self) -> bool:
        """
        Open the Raspberry Pi camera stream.
        """

        raise NotImplementedError(
            "Raspberry Pi camera integration is not implemented yet."
        )

    def read_frame(self):
        """
        Read one frame from the Raspberry Pi camera.
        """

        raise NotImplementedError(
            "Raspberry Pi camera frame reading is not implemented yet."
        )

    def release(self):
        """
        Release the Raspberry Pi camera resource.
        """

        raise NotImplementedError(
            "Raspberry Pi camera release is not implemented yet."
        )