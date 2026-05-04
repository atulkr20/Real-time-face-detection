from PIL import Image, ImageDraw
import numpy as np

def draw_bounding_box(frame_rgb: np.ndarray, roi: dict) -> np.ndarray:
    """
    Takes RGB numpy array + ROI dict.
    Draws axis-aligned minimal bounding box using Pillow (no OpenCV).
    Returns RGB numpy array with box drawn.
    """
    image = Image.fromarray(frame_rgb)
    draw = ImageDraw.Draw(image)

    x = roi["x"]
    y = roi["y"]
    w = roi["width"]
    h = roi["height"]

    # Draw rectangle — axis-aligned minimal bounding box
    draw.rectangle(
        [x, y, x + w, y + h],
        outline=(0, 255, 0),  # green box
        width=3
    )

    return np.array(image)