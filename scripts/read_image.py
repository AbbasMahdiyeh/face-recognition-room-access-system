"""
Load and inspect a real image using OpenCV.

This script demonstrates how OpenCV reads image
files and represents them as NumPy arrays.
"""

import cv2


def main():
    """
    Load an image and inspect its properties.
    """

    image_path = "data/sample_images/abbas.jpg"

    image = cv2.imread(image_path)

    if image is None:
        print("Failed to load image.")
        return

    print("Image shape:", image.shape)

    print("Image dtype:", image.dtype)

    cv2.imshow("Loaded Image", image)

    cv2.waitKey(0)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()