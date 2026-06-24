"""
MockTemperatureSensor verification script.
"""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
src_path = project_root / "src"

sys.path.insert(0, str(src_path))

from room_access.hardware.temperature_sensor import MockTemperatureSensor


def main():
    """
    Verify that the mock temperature sensor returns a temperature value.
    """

    sensor = MockTemperatureSensor(
        temperature_celsius=23.5,
    )

    temperature = sensor.read_temperature()

    print(f"Temperature: {temperature:.1f} °C")


if __name__ == "__main__":
    main()