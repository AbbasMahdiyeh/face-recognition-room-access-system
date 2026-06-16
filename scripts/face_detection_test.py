"""
Face detection test using OpenCV.

This script loads a real image, detects faces,
and draws bounding boxes around detected faces.
"""

import cv2
from pathlib import Path


def main():
    """
    Load a sample image and run face detection.
    """

    image_path = "data/sample_images/abbas.jpg"

    image = cv2.imread(image_path)

    if image is None:
        print("Failed to load image.")
        return

    print("Image loaded successfully.")
    print("Image shape:", image.shape)

    # Convert the image from BGR to grayscale because Haar Cascade
    # face detection works on intensity patterns rather than color.
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Load OpenCV's pre-trained Haar Cascade face detector.
    # This is a classical computer vision model, not deep learning.
    cascade_path = (
    Path(cv2.__file__).parent
    / "data"
    / "haarcascade_frontalface_default.xml"
)

    face_detector = cv2.CascadeClassifier(str(cascade_path))

    # Detect faces in the grayscale image.
    # Each detected face is returned as a rectangle: x, y, width, height.
    faces = face_detector.detectMultiScale(
        gray_image,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    print("Detected faces:", len(faces))

    '''
        # Draw a bounding box around each detected face.
        # This is the same visual feedback style used later for access decisions.
        # Each detected face is represented by a bounding box.
        # x and y define the top-left corner of the face region,
        # while w and h represent width and height.
    '''
    for (x, y, w, h) in faces:
        print(
            f"x={x}, y={y}, width={w}, height={h}"
        )

        # Ignore very small detections because they are more likely
        # to be false positives rather than real faces.
        if w < 120 or h < 120:
            continue

        image_height = image.shape[0]

        '''
            # Ignore detections that appear too low in the image.
            # In portrait-style images, the real face is usually located
            # in the upper half, while false positives may appear on clothes.
            # Temporary heuristic used to filter obvious
            # false positives in the current sample image.
            # This rule is not intended for production use.
        '''
        if y > image_height * 0.55:
            continue

        cv2.rectangle(
            image,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        # Crop the detected face region from the original image.
        # This cropped face can later be used for building an
        # authorized-user dataset or for face recognition.
        face_crop = image[y:y + h, x:x + w]

        # Store cropped face regions in a dedicated folder.
        # Keeping detection outputs separate from sample input images
        # makes the project structure cleaner and easier to debug.
        output_path = f"data/detected_faces/detected_face_{x}_{y}.png"
        
        cv2.imwrite(output_path, face_crop)
        print(f"Saved cropped face to: {output_path}")

    cv2.imshow("Detected Faces", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()