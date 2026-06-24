"""
MockLEDController verification script.
"""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
src_path = project_root / "src"

sys.path.insert(0, str(src_path))

from room_access.hardware.led_controller import MockLEDController


def main():
    """
    Verify granted and denied LED states.
    """

    controller = MockLEDController()

    print("Testing granted access:")
    controller.show_access_result(access_granted=True)

    print("Testing denied access:")
    controller.show_access_result(access_granted=False)


if __name__ == "__main__":
    main()