"""
AccessDecisionManager verification script.

This script verifies that raw recognition outputs are converted
into clean access-control decisions.
"""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
src_path = project_root / "src"

sys.path.insert(0, str(src_path))

from room_access.access_control.access_decision import AccessDecisionManager


def main():
    """
    Test granted and denied access decisions.
    """

    manager = AccessDecisionManager()

    granted_decision = manager.decide(
        user_name="abbas",
        access_granted=True,
    )

    denied_decision = manager.decide(
        user_name="abbas",
        access_granted=False,
    )

    unknown_decision = manager.decide(
        user_name=None,
        access_granted=False,
    )

    print("Granted:", granted_decision)
    print("Denied:", denied_decision)
    print("Unknown:", unknown_decision)


if __name__ == "__main__":
    main()