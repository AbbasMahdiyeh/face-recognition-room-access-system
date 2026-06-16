"""
OpenCV learning and verification script.

This script is intentionally separated from the
main application.

Its purpose is to verify that OpenCV is installed
correctly and to understand how images are
represented in memory.
"""

import cv2
import numpy as np


def main():
    """
    Verify OpenCV and NumPy installation.
    """

    print("OpenCV Version:", cv2.__version__)
    print("NumPy Version:", np.__version__)


if __name__ == "__main__":
    main()