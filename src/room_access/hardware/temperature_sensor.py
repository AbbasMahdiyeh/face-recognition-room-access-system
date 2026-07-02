"""
Temperature sensor implementations.

Purpose
-------
Provide temperature sensor backends for both development and
Raspberry Pi deployment.

Architecture
------------
The application always interacts with a temperature sensor through
the same public method:

    read_temperature()

This allows the hardware backend to be replaced without changing
the application logic.

Available implementations
-------------------------
- MockTemperatureSensor
    Used during laptop development.

- RaspberryPiTemperatureSensor
    Reads temperature from a real DS18B20 OneWire sensor connected
    to a Raspberry Pi.
"""

from pathlib import Path


class MockTemperatureSensor:
    """
    Simulate a room temperature sensor.
    """

    def __init__(
        self,
        temperature_celsius: float = 23.5,
    ):
        """
        Store a fixed mock temperature.

        Keeping a deterministic value makes dashboard development
        and testing possible before the physical hardware exists.
        """

        self.temperature_celsius = temperature_celsius

    def read_temperature(self) -> float:
        """
        Return the simulated room temperature.
        """

        return self.temperature_celsius


class RaspberryPiTemperatureSensor:
    """
    Read temperature from a DS18B20 OneWire sensor.

    Hardware
    --------
    VCC  -> 3.3V

    GND  -> GND

    DATA -> GPIO4

    A 4.7 kΩ pull-up resistor must be connected between DATA
    and 3.3V.
    """

    def __init__(
        self,
        devices_root: str = "/sys/bus/w1/devices",
    ):
        """
        Store the Linux OneWire devices directory.

        Every detected DS18B20 appears as a folder beginning with
        '28-'.
        """

        self.devices_root = Path(devices_root)

    def _find_temperature_file(self) -> Path | None:
        """
        Locate the DS18B20 temperature file.

        Returns
        -------
        Path
            Path to the temperature file.

        None
            If no compatible sensor is detected.
        """

        if not self.devices_root.exists():
            return None

        for device in self.devices_root.iterdir():

            if device.name.startswith("28-"):

                temperature_file = device / "temperature"

                if temperature_file.exists():
                    return temperature_file

        return None

    def read_temperature(self) -> float:
        """
        Read the current temperature in Celsius.

        Linux reports the DS18B20 temperature in milli-Celsius.

        Example
        -------
        25375

        becomes

        25.375 °C
        """

        temperature_file = self._find_temperature_file()

        if temperature_file is None:

            raise RuntimeError(
                "No DS18B20 temperature sensor was found. "
                "Verify the GPIO wiring, pull-up resistor, "
                "OneWire configuration, and reboot the Raspberry Pi."
            )

        raw_value = temperature_file.read_text(
            encoding="utf-8",
        ).strip()

        temperature_milli_celsius = int(raw_value)

        return temperature_milli_celsius / 1000.0