"""
CameraFactory verification script.

This script verifies that the configured camera backend
can be created from application settings.
"""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
src_path = project_root / "src"

sys.path.insert(0, str(src_path))

from room_access.camera.camera_factory import CameraFactory
from room_access.config.settings import Settings


def main():
    """
    Create the configured camera backend.
    """

    settings = Settings()

    camera = CameraFactory.create_camera(settings)

    print("Created camera:", camera.__class__.__name__)


if __name__ == "__main__":
    main()