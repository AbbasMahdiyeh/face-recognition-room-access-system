"""
Dashboard theme configuration.

This module centralizes all visual styling used by the
dashboard. Keeping colors and drawing parameters here
makes it easy to update the application's appearance
without modifying drawing logic.
"""

# ==========================
# Colors (OpenCV uses BGR)
# ==========================

AUTHORIZED_COLOR = (70, 210, 70)

UNAUTHORIZED_COLOR = (60, 70, 255)

TEXT_COLOR = (255, 255, 255)

SYSTEM_INFO_COLOR = AUTHORIZED_COLOR

BACKGROUND_COLOR = (15, 18, 18)

BORDER_COLOR = (70, 85, 85)

# ==========================
# Drawing parameters
# ==========================

DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720

STATUS_BAR_HEIGHT = 75

LINE_THICKNESS = 3
CORNER_LENGTH = 35
FONT_SCALE = 0.65
FONT_THICKNESS = 2