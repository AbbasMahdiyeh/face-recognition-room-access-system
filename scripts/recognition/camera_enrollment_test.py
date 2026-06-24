"""
Camera enrollment verification script.

This script starts EnrollmentApp for one user name provided
from the command line.

Example
-------
python scripts/recognition/camera_enrollment_test.py abbas_test
"""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
src_path = project_root / "src"

sys.path.insert(0, str(src_path))

from room_access.app.enrollment_app import EnrollmentApp


def main():
    """
    Start camera-based enrollment for one user.
    """

    if len(sys.argv) < 2:
        print("Usage: python scripts/recognition/camera_enrollment_test.py <user_name>")
        return

    user_name = sys.argv[1]

    app = EnrollmentApp(
        capture_count=5,
    )

    app.run(user_name)


if __name__ == "__main__":
    main()