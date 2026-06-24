"""
LED controller abstraction.

This module defines a mock LED controller for development.

Later, a Raspberry Pi GPIO-based controller can implement
the same behavior using real hardware pins.
"""


class MockLEDController:
    """
    Simulate access status LEDs.
    
    Green LED represents granted access.
    Red LED represents denied access.

    The controller remembers the last LED state so it only
    updates the output when the access status actually changes.
    """

    def __init__(self):
        """
        Store the last displayed access state.

        None means no LED state has been shown yet.
        """

        self.last_access_granted = None

    def show_access_result(
        self,
        access_granted: bool,
    ):
        """
        Show the access decision using simulated LEDs.

        Repeated identical states are ignored to avoid unnecessary
        hardware updates in the future Raspberry Pi implementation.
        """

        if access_granted == self.last_access_granted:
            return

        if access_granted:
            print("GREEN LED ON | RED LED OFF")
        else:
            print("GREEN LED OFF | RED LED ON")

        self.last_access_granted = access_granted