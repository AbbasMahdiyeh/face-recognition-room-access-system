"""
Raspberry Pi GPIO LED controller.

Platform Note
-------------
This module targets Raspberry Pi hardware.

It is intentionally included in the project during development so the
complete hardware architecture is visible before deployment.

On non-Raspberry Pi systems this module is expected to remain unused.
The application will use MockLEDController instead.

Purpose
-------
This controller manages the real green and red status LEDs connected
to Raspberry Pi GPIO pins.

It exposes the same public interface as MockLEDController, allowing
the application to switch between development and production hardware
without changing the application logic.
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