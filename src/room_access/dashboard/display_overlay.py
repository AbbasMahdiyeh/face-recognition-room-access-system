"""
Display overlay utilities.

This module draws recognition results on image frames.

It is responsible only for visualization:
- drawing face bounding boxes
- showing the recognized user name
- showing access status text

It does not perform recognition or make access decisions.
"""

import cv2

from room_access.recognition.recognition_engine import RecognitionResult

def draw_corner_box(
    image,
    bbox: tuple[int, int, int, int],
    color: tuple[int, int, int],
    thickness: int = 3,
    corner_length: int = 35,
):
    """
    Draw a modern corner-style bounding box.

    Corner boxes look cleaner than full rectangles and keep
    the face area less visually cluttered.
    """

    x1, y1, x2, y2 = bbox

    # Top-left corner
    cv2.line(image, (x1, y1), (x1 + corner_length, y1), color, thickness)
    cv2.line(image, (x1, y1), (x1, y1 + corner_length), color, thickness)

    # Top-right corner
    cv2.line(image, (x2, y1), (x2 - corner_length, y1), color, thickness)
    cv2.line(image, (x2, y1), (x2, y1 + corner_length), color, thickness)

    # Bottom-left corner
    cv2.line(image, (x1, y2), (x1 + corner_length, y2), color, thickness)
    cv2.line(image, (x1, y2), (x1, y2 - corner_length), color, thickness)

    # Bottom-right corner
    cv2.line(image, (x2, y2), (x2 - corner_length, y2), color, thickness)
    cv2.line(image, (x2, y2), (x2, y2 - corner_length), color, thickness)


def draw_filled_label(
    image,
    text: str,
    bbox: tuple[int, int, int, int],
    color: tuple[int, int, int],
):
    """
    Draw a centered label above the face bounding box.

    Centering the label makes the overlay look cleaner and
    keeps the identity information visually connected to the face.
    """

    x1, y1, x2, _ = bbox

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.65
    thickness = 2
    padding_x = 12
    padding_y = 8

    text_size, _ = cv2.getTextSize(
        text,
        font,
        font_scale,
        thickness,
    )

    text_width, text_height = text_size
    face_center_x = (x1 + x2) // 2

    label_width = text_width + padding_x * 2
    label_height = text_height + padding_y * 2

    label_x1 = face_center_x - label_width // 2
    label_y1 = max(y1 - label_height - 8, 0)
    label_x2 = label_x1 + label_width
    label_y2 = label_y1 + label_height

    cv2.rectangle(
        image,
        (label_x1, label_y1),
        (label_x2, label_y2),
        color,
        -1,
    )

    cv2.putText(
        image,
        text,
        (label_x1 + padding_x, label_y2 - padding_y),
        font,
        font_scale,
        (255, 255, 255),
        thickness,
    )

def draw_recognition_overlay(
    image,
    result: RecognitionResult,
):
    """
    Draw visual feedback for a recognition result.

    Green indicates granted access.
    Red indicates denied access or an unknown user.
    """

    annotated_image = image.copy()

    if result.access_granted:
        color = (80, 180, 80)
        user_label = result.user_name or "Unknown"
        access_label = "ACCESS GRANTED"
    else:
        color = (80, 80, 220)
        user_label = "Unknown"
        access_label = "ACCESS DENIED"

    bbox = result.bbox

    if bbox is not None:
        x1, y1, x2, y2 = bbox

        label_text = (
            f"ID: {user_label} | AUTHORIZED"
            if result.access_granted
            else "ID: UNKNOWN | UNAUTHORIZED"
        )

        draw_corner_box(
            annotated_image,
            bbox,
            color,
        )

        draw_filled_label(
            annotated_image,
            label_text,
            bbox,
            color,
        )

    height = annotated_image.shape[0]

    height, width = annotated_image.shape[:2]
    bar_height = 65

    cv2.rectangle(
        annotated_image,
        (0, height - bar_height),
        (width, height),
        color,
        -1,
    )

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.0
    thickness = 2

    text_size, _ = cv2.getTextSize(
        access_label,
        font,
        font_scale,
        thickness,
    )

    text_width, text_height = text_size

    text_x = (width - text_width) // 2
    text_y = height - (bar_height - text_height) // 2

    cv2.putText(
        annotated_image,
        access_label,
        (text_x, text_y),
        font,
        font_scale,
        (255, 255, 255),
        thickness,
    )

    return annotated_image