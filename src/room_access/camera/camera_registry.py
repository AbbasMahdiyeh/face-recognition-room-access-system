"""
Camera backend registry.

Why does this module exist?
---------------------------
As the project grows, new camera backends will be added
(e.g. USB cameras, Raspberry Pi cameras, IP cameras, RTSP streams).

Without a registry, CameraFactory would continuously grow with
large if/elif blocks, making it difficult to maintain.

The registry follows the Open/Closed Principle:

- Open for extension:
    New camera backends can be added.

- Closed for modification:
    Existing factory logic does not need to change.

This keeps the architecture scalable and easy to maintain.
"""

from room_access.camera.laptop_webcam_camera import LaptopWebcamCamera
from room_access.camera.raspberry_pi_camera import RaspberryPiCamera


CAMERA_REGISTRY = {
    "laptop": LaptopWebcamCamera,
    "raspberry_pi": RaspberryPiCamera,
}