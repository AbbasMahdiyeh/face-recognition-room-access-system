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
This module is intended to run on Raspberry Pi systems with
gpiozero installed.

Development Note
----------------
gpiozero is a Raspberry Pi-oriented GPIO library.

The import is wrapped in a try/except block so the project remains
importable and developable on non-Raspberry Pi platforms such as Windows.

Implementation Note
-------------------
gpiozero was selected because it was successfully validated with the
actual project LED wiring during Raspberry Pi hardware setup.
"""

# gpiozero is only available on Raspberry Pi.
# During Windows development this import is expected to be unresolved.
try:
    from gpiozero import LED
    GPIOZERO_AVAILABLE = True

except ImportError:
    LED = None
    GPIOZERO_AVAILABLE = False


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

        if not GPIOZERO_AVAILABLE:
            raise RuntimeError(
                "gpiozero is not available. "
                "This controller can only run on Raspberry Pi. "
                "Use MockLEDController on non-Raspberry Pi systems."
            )
        
        assert LED is not None

        self.green_led = LED(green_pin)
        self.red_led = LED(red_pin)
        self.last_access_granted = None

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
            self.green_led.on()
            self.red_led.off()
        else:
            self.green_led.off()
            self.red_led.on()

        self.last_access_granted = access_granted

    def turn_off(self):
        """
        Turn both LEDs off.
        """

        self.green_led.off()
        self.red_led.off()

    def cleanup(self):
        """
        Turn off LEDs before application shutdown.
        """

        self.turn_off()