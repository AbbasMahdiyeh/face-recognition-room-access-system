"""
Image-based camera implementation.

Loads frames from image files for development
and testing without physical hardware.
"""

from .camera_interface import CameraInterface


class ImageCamera(CameraInterface):
    """
    Camera implementation that uses image files
    as the frame source.
    """

    def __init__(self, image_path: str):
        self.image_path = image_path

    def get_frame(self):
        """
        Return a frame loaded from an image file.

        Implementation will be completed after
        OpenCV integration.
        """
        raise NotImplementedError(
            "Image loading is not implemented yet."
        )