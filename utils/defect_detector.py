import cv2
import numpy as np

def detect_defect(image, mode="canny", canny_low=30, canny_high=150, block_size=11, c_value=2):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    result = image.copy()

    if mode == "canny":
        equalized = cv2.equalizeHist(gray)
        blurred = cv2.GaussianBlur(equalized, (3, 3), 0)
        edges = cv2.Canny(blurred, canny_low, canny_high)

    elif mode == "adaptive":
        if block_size % 2 == 0:
            block_size += 1
        edges = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            block_size,
            c_value
        )

    elif mode == "otsu":
        _, edges = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    elif mode == "morph":
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        edges = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel)

    else:
        raise ValueError("Invalid mode: choose 'canny', 'adaptive', 'otsu', or 'morph'")

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        if cv2.contourArea(cnt) > 50:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return result, len(contours), edges
