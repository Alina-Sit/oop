import math
import tkinter as tk

SIZE = 24


def _dot(img, x, y):
    img.put("black", to=(x, y, x + 2, y + 2))


def make_icon(kind):
    img = tk.PhotoImage(width=SIZE, height=SIZE)

    if kind == "point":
        cx, cy = 12, 12
        for dx in range(-4, 5):
            for dy in range(-4, 5):
                if dx * dx + dy * dy <= 16:
                    img.put("black", to=(cx + dx, cy + dy))

    elif kind == "line":
        for t in range(16):
            _dot(img, 3 + t, 19 - t)

    elif kind == "rectangle":
        for x in range(4, 20):
            _dot(img, x, 6)
            _dot(img, x, 16)
        for y in range(6, 18):
            _dot(img, 4, y)
            _dot(img, 19, y)

    elif kind == "ellipse":
        for a in range(0, 360, 3):
            x = 11 + round(8 * math.cos(math.radians(a)))
            y = 11 + round(6 * math.sin(math.radians(a)))
            _dot(img, x, y)

    return img