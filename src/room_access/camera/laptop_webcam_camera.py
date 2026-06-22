"""
Laptop webcam camera backend.

This module provides a camera implementation based on
OpenCV's VideoCapture.

It is used for development and testing on a laptop before
deploying the same recognition pipeline to Raspberry Pi.
"""

import cv2


class LaptopWebcamCamera:
    """
    Read live frames from a laptop or USB webcam.
    """

    def __init__(self, camera_index: int = 0):
        """
        Store the webcam index.

        camera_index=0 usually refers to the default built-in
        laptop webcam. External USB cameras may use index 1 or higher.
        """

        self.camera_index = camera_index
        self.capture = None

    def open(self) -> bool:
        """
        Open the webcam stream.

        Returns True if the camera is available.
        """

        self.capture = cv2.VideoCapture(self.camera_index)

        return self.capture.isOpened()

    def read_frame(self):
        """
        Read one frame from the webcam.

        Returns None if the camera is not open or if a frame
        cannot be captured.
        """

        if self.capture is None:
            return None

        success, frame = self.capture.read()

        if not success:
            return None

        return frame

    def release(self):
        """
        Release the webcam resource.

        This should always be called when the application ends
        so the operating system can free the camera device.
        """

        if self.capture is not None:
            self.capture.release()
            self.capture = None