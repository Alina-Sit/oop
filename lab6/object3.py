import math
import tkinter as tk
from tkinter import ttk

from ipc import MessageServer, PORT_OBJECT3

MARGIN_LEFT = 60
MARGIN_RIGHT = 25
MARGIN_TOP = 30
MARGIN_BOTTOM = 45


def nice_step(span, parts):
    raw = span / parts
    power = 10 ** math.floor(math.log10(raw))
    for k in (1, 2, 5, 10):
        if raw <= k * power:
            return k * power
    return 10 * power


def ticks(low, high, parts):
    step = nice_step(high - low, parts)
    first = math.ceil(low / step) * step
    result = []
    value = first
    while value <= high + step * 1e-9:
        result.append(round(value, 10))
        value += step
    return result


class Object3:
    def __init__(self, root):
        self.root = root
        root.title("Object3 — графік")
        root.geometry("640x500+500+20")

        self.info = tk.StringVar(value="Чекаю команду від Lab6...")
        ttk.Label(root, textvariable=self.info, font=("Arial", 11)).pack(pady=6)
        self.canvas = tk.Canvas(root, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.canvas.bind("<Configure>", lambda e: self.redraw())

        self.values = []
        self.server = MessageServer(PORT_OBJECT3, self.on_message)
        self.server.start(root)
        root.protocol("WM_DELETE_WINDOW", self.quit)

    def on_message(self, msg):
        cmd = msg.get("cmd")
        if cmd == "ping":
            return {"ok": True, "name": "Object3"}
        if cmd == "place":
            self.place(msg.get("geometry"))
            return {"ok": True}
        if cmd == "plot":
            return self.plot(msg.get("geometry"))
        if cmd == "quit":
            self.root.after(100, self.quit)
            return {"ok": True}
        return {"ok": False, "error": "невідома команда"}

    def place(self, geometry):
        if geometry:
            self.root.geometry(geometry)
        self.root.deiconify()
        self.root.lift()

    def read_clipboard(self):
        try:
            text = self.root.clipboard_get()
        except tk.TclError:
            raise ValueError("буфер обміну порожній")
        try:
            return [float(part.replace(",", ".")) for part in text.split()]
        except ValueError:
            raise ValueError("у буфері обміну не числа")

    def plot(self, geometry):
        values = self.read_clipboard()
        if not values:
            raise ValueError("у буфері обміну немає даних")
        self.values = values
        self.info.set(f"Графік y = f(x), точок: {len(values)}")
        self.place(geometry)
        self.root.update_idletasks()
        self.redraw()
        return {"ok": True, "count": len(values)}

    def redraw(self):
        c = self.canvas
        c.delete("all")
        if not self.values:
            return
        w, h = c.winfo_width(), c.winfo_height()
        left, right = MARGIN_LEFT, w - MARGIN_RIGHT
        top, bottom = MARGIN_TOP, h - MARGIN_BOTTOM
        if right - left < 50 or bottom - top < 50:
            return

        xs = list(range(len(self.values)))
        xmin, xmax = 0, max(1, len(xs) - 1)
        ymin, ymax = min(self.values), max(self.values)
        if ymin == ymax:
            ymin, ymax = ymin - 1, ymax + 1
        pad = (ymax - ymin) * 0.05
        ymin, ymax = ymin - pad, ymax + pad

        def px(x):
            return left + (x - xmin) / (xmax - xmin) * (right - left)

        def py(y):
            return bottom - (y - ymin) / (ymax - ymin) * (bottom - top)

        for x in ticks(xmin, xmax, 8):
            c.create_line(px(x), top, px(x), bottom, fill="#e3e3e3")
            c.create_line(px(x), bottom, px(x), bottom + 4)
            c.create_text(px(x), bottom + 15, text=f"{x:g}", font=("Arial", 9))
        for y in ticks(ymin, ymax, 6):
            c.create_line(left, py(y), right, py(y), fill="#e3e3e3")
            c.create_line(left - 4, py(y), left, py(y))
            c.create_text(left - 8, py(y), text=f"{y:.2f}", anchor="e", font=("Arial", 9))

        c.create_line(left, bottom, right, bottom, width=2)
        c.create_line(left, top, left, bottom, width=2)
        c.create_text(right, bottom + 32, text="x (індекс)", anchor="e", font=("Arial", 9, "italic"))
        c.create_text(left, top - 14, text="y", anchor="w", font=("Arial", 9, "italic"))

        points = []
        for x, y in zip(xs, self.values):
            points.extend((px(x), py(y)))
        if len(xs) > 1:
            c.create_line(*points, fill="blue", width=2)
        for i in range(0, len(points), 2):
            c.create_oval(points[i] - 3, points[i + 1] - 3, points[i] + 3, points[i + 1] + 3,
                          fill="blue", outline="blue")

    def quit(self):
        self.server.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    try:
        Object3(root)
    except OSError:
        print("Object3 вже запущений")
        root.destroy()
    else:
        root.mainloop()
