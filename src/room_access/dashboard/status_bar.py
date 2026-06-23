import cv2

from room_access.dashboard.theme import (
    AUTHORIZED_COLOR,
    UNAUTHORIZED_COLOR,
    BACKGROUND_COLOR,
    TEXT_COLOR,
    STATUS_BAR_HEIGHT,
)


def draw_status_bar(
    image,
    text: str,
    color: tuple[int, int, int],
    access_granted: bool,
):
    height, width = image.shape[:2]

    y1 = height - STATUS_BAR_HEIGHT - 15
    y2 = height - 15
    x1 = 25
    x2 = width - 25

    cv2.rectangle(image, (x1, y1), (x2, y2), BACKGROUND_COLOR, -1)
    cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

    icon_x = x1 + 90
    icon_y = (y1 + y2) // 2

    icon_color = AUTHORIZED_COLOR if access_granted else UNAUTHORIZED_COLOR

    cv2.circle(image, (icon_x, icon_y), 24, icon_color, 3)

    if access_granted:
        cv2.line(image, (icon_x - 11, icon_y), (icon_x - 3, icon_y + 8), icon_color, 4)
        cv2.line(image, (icon_x - 3, icon_y + 8), (icon_x + 13, icon_y - 12), icon_color, 4)
    else:
        cv2.line(image, (icon_x - 11, icon_y - 11), (icon_x + 11, icon_y + 11), icon_color, 4)
        cv2.line(image, (icon_x + 11, icon_y - 11), (icon_x - 11, icon_y + 11), icon_color, 4)

    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = 1.0
    thickness = 2

    text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
    text_x = (width - text_size[0]) // 2
    text_y = icon_y + text_size[1] // 2

    cv2.putText(
        image,
        text,
        (text_x, text_y),
        font,
        font_scale,
        icon_color,
        thickness,
    )