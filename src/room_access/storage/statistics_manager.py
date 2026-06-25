"""
Access statistics manager.

This module reads access event logs and generates simple
summary statistics for presentation and system monitoring.
"""

import csv
from pathlib import Path


class StatisticsManager:
    """
    Generate access-control statistics from the CSV event log.
    """

    def __init__(
        self,
        log_path: str = "data/logs/access_events.csv",
    ):
        self.log_path = Path(log_path)

    def get_summary(self) -> dict:
        """
        Return a summary of recorded access events.
        """

        if not self.log_path.exists():
            return {
                "total_events": 0,
                "granted": 0,
                "denied": 0,
                "last_event": None,
            }

        total_events = 0
        granted = 0
        denied = 0
        last_event = None

        with self.log_path.open(
            mode="r",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)

            for row in reader:
                total_events += 1
                last_event = row

                if row["access_granted"] == "True":
                    granted += 1
                else:
                    denied += 1

        return {
            "total_events": total_events,
            "granted": granted,
            "denied": denied,
            "last_event": last_event,
        }