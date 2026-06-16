"""
Camera interface definition.

Every camera implementation in the project must
follow this contract.
"""

from abc import ABC, abstractmethod


class CameraInterface(ABC):
    """
    Abstract base class for all camera sources.
    """

    @abstractmethod
    def get_frame(self):
        """
        Return a single image frame.
        """
        pass