"""
Camera interface definition.

Every camera implementation in the project must follow this contract.
This allows the application to switch between laptop webcam,
USB camera, and Raspberry Pi camera backends without changing
the application workflow.
"""

from abc import ABC, abstractmethod


class CameraInterface(ABC):
    """
    Abstract base class for all camera sources.
    """

    @abstractmethod
    def open(self) -> bool:
        """
        Open the camera stream.
        """

        pass

    @abstractmethod
    def read_frame(self):
        """
        Read and return a single image frame.
        """

        pass

    @abstractmethod
    def release(self):
        """
        Release the camera resource.
        """

        pass