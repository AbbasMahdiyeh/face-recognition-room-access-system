"""
LiveAccessApp verification script.

This script starts the real-time access-control application.
The actual workflow lives inside src/room_access/app/live_access_app.py.
"""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
src_path = project_root / "src"

sys.path.insert(0, str(src_path))

from room_access.app.live_access_app import LiveAccessApp


def main():
    """
    Start the live access-control application.
    """

    app = LiveAccessApp()
    app.run()


if __name__ == "__main__":
    main()