import math
import tkinter as tk

SIZE = 24


def _dot(img, x, y):
    img.put("black", to=(x, y, x + 2, y + 2))


def _line(img, x1, y1, x2, y2):
    steps = max(abs(x2 - x1), abs(y2 - y1), 1)
    for i in range(steps + 1):
        _dot(img, round(x1 + (x2 - x1) * i / steps), round(y1 + (y2 - y1) * i / steps))


def _rect(img, x1, y1, x2, y2):
    _line(img, x1, y1, x2, y1)
    _line(img, x1, y2, x2, y2)
    _line(img, x1, y1, x1, y2)
    _line(img, x2, y1, x2, y2)


def _ellipse(img, cx, cy, rx, ry):
    for a in range(0, 360, 3):
        _dot(img, cx + round(rx * math.cos(math.radians(a))),
             cy + round(ry * math.sin(math.radians(a))))


def _draw_point(img):
    for dx in range(-4, 5):
        for dy in range(-4, 5):
            if dx * dx + dy * dy <= 16:
                img.put("black", to=(12 + dx, 12 + dy))


def _draw_line(img):
    _line(img, 3, 19, 18, 4)


def _draw_rectangle(img):
    _rect(img, 4, 6, 19, 16)


def _draw_ellipse(img):
    _ellipse(img, 11, 11, 8, 6)


def _draw_line_circles(img):
    _line(img, 6, 17, 16, 7)
    _ellipse(img, 5, 18, 3, 3)
    _ellipse(img, 17, 6, 3, 3)


def _draw_cube(img):
    _rect(img, 3, 9, 14, 20)
    _rect(img, 9, 3, 20, 14)
    _line(img, 3, 9, 9, 3)
    _line(img, 14, 9, 20, 3)
    _line(img, 3, 20, 9, 14)
    _line(img, 14, 20, 20, 14)


DRAWERS = {
    "point": _draw_point,
    "line": _draw_line,
    "rectangle": _draw_rectangle,
    "ellipse": _draw_ellipse,
    "line_circles": _draw_line_circles,
    "cube": _draw_cube,
}


def make_icon(kind):
    drawer = DRAWERS.get(kind)
    if drawer is None:
        return None
    img = tk.PhotoImage(width=SIZE, height=SIZE)
    drawer(img)
    return img
