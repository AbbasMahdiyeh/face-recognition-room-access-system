"""
Understanding image representation in OpenCV.

This script creates a synthetic image and
demonstrates how images are stored as NumPy arrays.
"""

import cv2
import numpy as np


def main():
    """
    Create a simple black image and inspect its properties.
    """

    image = np.zeros((300, 400, 3), dtype=np.uint8)

    # Demonstrates direct pixel manipulation by coloring a
    # rectangular region of the image in blue (BGR format).
    image[50:150, 100:300] = (255, 0, 0)

    # Inspect pixel values at different locations.
    print("Black pixel:", image[10, 10])
    print("Blue pixel:", image[75, 150])

    # Demonstrates OpenCV's built-in drawing functions.
    # Bounding boxes around detected faces will be drawn
    # using the same mechanism later in the project.
    cv2.rectangle(image, (50, 200), (350, 260), (0, 255, 0), 3)

    print("Image shape:", image.shape)
    print("Image data type:", image.dtype)

    # Demonstrates text rendering on image frames.
    # Future access-control decisions will be visualized
    # using similar text overlays.
    cv2.putText(
        image,
        "Access Granted",
        (70, 180),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    # Demonstrates OpenCV circle drawing.
    # Similar overlays can later highlight regions
    # of interest detected by computer vision models.
    cv2.circle(
        image,
        (200, 150),
        40,
        (0, 0, 255),
        3
    )

    # Demonstrates line rendering in OpenCV.
    # Useful for visual debugging and annotation tasks.
    cv2.line(
        image,
        (0, 0),
        (400, 300),
        (255, 255, 255),
        2
    )

    # Save the generated image to disk.
    # This demonstrates how OpenCV can export processed
    # frames and visualizations.
    output_path = "data/sample_images/opencv_drawing_demo.png"
    cv2.imwrite(output_path, image)
    print(f"Image saved to: {output_path}")
    cv2.imshow("Black Image", image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()