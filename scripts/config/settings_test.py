"""
Settings verification script.
"""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
src_path = project_root / "src"

sys.path.insert(0, str(src_path))

from room_access.config.settings import Settings


def main():
    settings = Settings()

    print("Threshold:", settings.get("recognition", "threshold"))
    print("Recognition interval:", settings.get("recognition", "recognition_interval"))
    print("Capture count:", settings.get("enrollment", "capture_count"))
    print("Display size:", settings.get("display", "width"), "x", settings.get("display", "height"))
    print("Camera:", settings.get("camera", "name"))


if __name__ == "__main__":
    main()