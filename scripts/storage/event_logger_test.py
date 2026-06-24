"""
EventLogger verification script.

This script verifies that access-control events can be
written to a CSV log file.
"""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
src_path = project_root / "src"

sys.path.insert(0, str(src_path))

from room_access.storage.event_logger import EventLogger


def main():
    """
    Write a sample access-control event.
    """

    logger = EventLogger(
        log_path="data/logs/test_access_events.csv"
    )

    logger.log_event(
        user_name="abbas",
        access_granted=True,
        similarity=0.9876,
        camera="Laptop Webcam",
        fps=18.5,
        recognition_time_ms=52.3,
        temperature="--",
    )

    print("Test event logged successfully.")
    print("Log path: data/logs/test_access_events.csv")


if __name__ == "__main__":
    main()