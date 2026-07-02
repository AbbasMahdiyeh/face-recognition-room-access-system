"""
Camera factory.

This module creates camera backends from application settings.

The factory does not import or manually select every camera class.
Instead, it delegates backend lookup to CAMERA_REGISTRY.

Why this matters:
- LiveAccessApp stays independent from concrete camera classes.
- New camera backends can be added with minimal changes.
- The project remains scalable as hardware support grows.
"""

from room_access.camera.camera_registry import CAMERA_REGISTRY


class CameraFactory:
    """
    Create camera backends from configuration.
    """

    @staticmethod
    def create_camera(settings):
        """
        Create the configured camera backend.

        The selected backend comes from config/settings.json.

        Example:
            "camera": {
                "backend": "laptop"
            }

        If a new backend is added later, it only needs to be
        registered in CAMERA_REGISTRY.
        """

        backend = settings.get(
            "camera",
            "backend",
            "laptop",
        )

        camera_class = CAMERA_REGISTRY.get(backend)

        if camera_class is None:
            available_backends = ", ".join(CAMERA_REGISTRY.keys())

            raise ValueError(
                f"Unknown camera backend: {backend}. "
                f"Available backends: {available_backends}"
            )

        if backend == "laptop":
            camera_index = settings.get(
                "camera",
                "index",
                0,
            )

            return camera_class(
                camera_index=camera_index,
            )

        if backend == "raspberry_pi":
            width = settings.get(
                "display",
                "width",
                1280,
            )

            height = settings.get(
                "display",
                "height",
                720,
            )

            return camera_class(
                width=width,
                height=height,
            )

        return camera_class()