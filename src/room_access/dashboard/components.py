"""
Reusable dashboard UI components.
"""

import cv2


def draw_panel(
    image,
    top_left,
    bottom_right,
    color,
):
    """
    Draw a reusable dashboard panel.

    Parameters
    ----------
    image
        Target image.

    top_left
        (x, y)

    bottom_right
        (x, y)

    color
        Panel background color.
    """

    cv2.rectangle(
        image,
        top_left,
        bottom_right,
        color,
        -1,
    )

def draw_info_icon(
    image,
    icon_type: str,
    center: tuple[int, int],
    color: tuple[int, int, int],
    scale: float = 1.0,
):
    """
    Draw a simple vector icon using OpenCV primitives.

    Icons are drawn directly with OpenCV so the dashboard
    does not depend on external image assets.
    """

    x, y = center
    s = scale

    if icon_type == "camera":
        cv2.rectangle(image, (int(x - 10*s), int(y - 7*s)), (int(x + 8*s), int(y + 7*s)), color, -1)
        cv2.circle(image, (x, y), int(4*s), (255, 255, 255), -1)
        cv2.rectangle(image, (int(x + 8*s), int(y - 4*s)), (int(x + 15*s), int(y + 4*s)), color, -1)

    elif icon_type == "fps":
        cv2.circle(image, (x, y), int(12*s), color, 2)
        cv2.line(image, (x, y), (int(x + 7*s), int(y - 7*s)), color, 2)

    elif icon_type == "faces":
        cv2.circle(image, (int(x - 6*s), int(y - 5*s)), int(5*s), color, -1)
        cv2.circle(image, (int(x + 7*s), int(y - 5*s)), int(5*s), color, -1)
        cv2.ellipse(image, (int(x - 6*s), int(y + 8*s)), (int(8*s), int(6*s)), 0, 180, 360, color, -1)
        cv2.ellipse(image, (int(x + 7*s), int(y + 8*s)), (int(8*s), int(6*s)), 0, 180, 360, color, -1)

    elif icon_type == "time":
        cv2.circle(image, (x, y), int(12*s), color, 2)
        cv2.line(image, (x, y), (x, int(y - 7*s)), color, 2)
        cv2.line(image, (x, y), (int(x + 6*s), int(y + 4*s)), color, 2)

    elif icon_type == "temperature":
        cv2.circle(image, (x, int(y + 8*s)), int(5*s), color, -1)
        cv2.rectangle(image, (int(x - 3*s), int(y - 12*s)), (int(x + 3*s), int(y + 8*s)), color, 2)