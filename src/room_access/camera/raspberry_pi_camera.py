"""
Raspberry Pi camera implementation.

Purpose
-------
Capture frames from the Raspberry Pi Camera Module using Picamera2.

Architecture
------------
This class implements the same public camera interface used by the
laptop webcam backend:

- open()
- read_frame()
- release()

Because all camera backends follow the same interface, LiveAccessApp
can switch between laptop webcam and Raspberry Pi camera through
CameraFactory without changing the application workflow.

Platform
--------
This module is intended to run on Raspberry Pi OS with Picamera2
installed.

Development Note
----------------
Picamera2 is only available on Raspberry Pi systems. The import is
wrapped in a try/except block so the project remains importable during
Windows development.
"""

import cv2

from .camera_interface import CameraInterface

try:
    from picamera2 import Picamera2  # type: ignore
except ImportError:
    Picamera2 = None


class RaspberryPiCamera(CameraInterface):
    """
    Capture image frames from the Raspberry Pi Camera Module.
    """

    def __init__(
        self,
        width: int = 1280,
        height: int = 720,
    ):
        """
        Store camera resolution settings.

        The actual Picamera2 object is created in open() so the camera
        resource is only allocated when the application starts.
        """

        self.width = width
        self.height = height
        self.camera = None

    def open(self) -> bool:
        """
        Open and start the Raspberry Pi camera stream.
        """

        if Picamera2 is None:
            print("Picamera2 is not installed or not available.")
            return False

        self.camera = Picamera2()

        config = self.camera.create_preview_configuration(
            main={
                "size": (self.width, self.height),
                "format": "RGB888",
            }
        )

        self.camera.configure(config)
        self.camera.start()

        return True

    def read_frame(self):
        """
        Read one frame from the Raspberry Pi camera.

        Picamera2 returns RGB frames, while OpenCV uses BGR frames.
        The conversion keeps the rest of the computer vision pipeline
        consistent with the laptop webcam backend.
        """

        if self.camera is None:
            return None

        frame = self.camera.capture_array()

        if frame is None:
            return None

        return cv2.cvtColor(
            frame,
            cv2.COLOR_RGB2BGR,
        )

    def release(self):
        """
        Stop the camera stream and release the camera resource.
        """

        if self.camera is not None:
            self.camera.stop()
            self.camera = None