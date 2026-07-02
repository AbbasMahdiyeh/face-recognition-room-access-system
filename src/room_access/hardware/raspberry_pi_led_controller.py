"""
Raspberry Pi GPIO LED controller.

Purpose
-------
Control the physical access indicator LEDs connected to the
Raspberry Pi GPIO header.

Architecture
------------
The application communicates with this controller only through
its public methods.

Because this class exposes the same interface as MockLEDController,
the active hardware backend can be selected dynamically through the
HardwareFactory without modifying the application logic.

Platform
--------
This module is intended to run only on Raspberry Pi systems with
the RPi.GPIO library installed.

Development Note
----------------
The RPi.GPIO package is available only on Raspberry Pi systems.

For this reason, the import is wrapped in a try/except block so the
entire project remains importable and fully developable on non-
Raspberry Pi platforms such as Windows.

Implementation Note
-------------------
RPi.GPIO was selected as the GPIO backend because it provides a
lightweight and reliable interface for the hardware used in this
project.

The implementation has been validated on the target Raspberry Pi
hardware during the hardware integration phase.
"""

try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True

except ImportError:
    GPIO = None
    GPIO_AVAILABLE = False


class RaspberryPiLEDController:
    """
    Control access status LEDs using Raspberry Pi GPIO pins.
    """

    def __init__(
        self,
        green_pin: int,
        red_pin: int,
    ):
        """
        Initialize GPIO pins for access feedback.

        green_pin is turned on when access is granted.
        red_pin is turned on when access is denied.
        """

        if not GPIO_AVAILABLE:
            raise RuntimeError(
                "RPi.GPIO is not available. "
                "This controller can only run on Raspberry Pi."
                "Use MockLEDController on non-Raspberry Pi systems."
            )

        self.green_pin = green_pin
        self.red_pin = red_pin
        self.last_access_granted = None

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.green_pin, GPIO.OUT)
        GPIO.setup(self.red_pin, GPIO.OUT)

        self.turn_off()

    def show_access_result(
        self,
        access_granted: bool,
    ):
        """
        Update LEDs only when the access state changes.
        """

        if access_granted == self.last_access_granted:
            return

        if access_granted:
            GPIO.output(self.green_pin, GPIO.HIGH)
            GPIO.output(self.red_pin, GPIO.LOW)
        else:
            GPIO.output(self.green_pin, GPIO.LOW)
            GPIO.output(self.red_pin, GPIO.HIGH)

        self.last_access_granted = access_granted

    def turn_off(self):
        """
        Turn both LEDs off.
        """

        GPIO.output(self.green_pin, GPIO.LOW)
        GPIO.output(self.red_pin, GPIO.LOW)

    def cleanup(self):
        """
        Release GPIO resources safely.
        """

        self.turn_off()
        GPIO.cleanup()