import random
import tkinter as tk
from tkinter import ttk

from ipc import MessageServer, PORT_OBJECT2

COLUMNS = 5


class Object2:
    def __init__(self, root):
        self.root = root
        root.title("Object2 — вектор")
        root.geometry("460x400+20+300")

        self.info = tk.StringVar(value="Чекаю команду від Lab6...")
        ttk.Label(root, textvariable=self.info, font=("Arial", 11)).pack(pady=8)

        cols = ["row"] + [f"c{i}" for i in range(COLUMNS)]
        self.tree = ttk.Treeview(root, columns=cols, show="headings")
        self.tree.heading("row", text="№")
        self.tree.column("row", width=50, anchor="center")
        for i in range(COLUMNS):
            self.tree.heading(f"c{i}", text=f"№{i + 1}")
            self.tree.column(f"c{i}", width=80, anchor="e")
        scroll = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True, padx=(8, 0), pady=(0, 8))

        self.vector = []
        self.server = MessageServer(PORT_OBJECT2, self.on_message)
        self.server.start(root)
        root.protocol("WM_DELETE_WINDOW", self.quit)

    def on_message(self, msg):
        cmd = msg.get("cmd")
        if cmd == "ping":
            return {"ok": True, "name": "Object2"}
        if cmd == "place":
            self.place(msg.get("geometry"))
            return {"ok": True}
        if cmd == "generate":
            return self.generate(int(msg["n"]), float(msg["min"]), float(msg["max"]), msg.get("geometry"))
        if cmd == "quit":
            self.root.after(100, self.quit)
            return {"ok": True}
        return {"ok": False, "error": "невідома команда"}

    def place(self, geometry):
        if geometry:
            self.root.geometry(geometry)
        self.root.deiconify()
        self.root.lift()

    def generate(self, n, low, high, geometry):
        if n < 1:
            return {"ok": False, "error": "n має бути більше 0"}
        if low > high:
            low, high = high, low
        self.vector = [random.uniform(low, high) for _ in range(n)]
        self.show_vector(low, high)
        self.place(geometry)
        self.to_clipboard()
        return {"ok": True, "count": n}

    def show_vector(self, low, high):
        self.info.set(f"Вектор з {len(self.vector)} чисел, діапазон [{low:g}; {high:g}]")
        self.tree.delete(*self.tree.get_children())
        for start in range(0, len(self.vector), COLUMNS):
            part = self.vector[start:start + COLUMNS]
            cells = [f"{v:.3f}" for v in part] + [""] * (COLUMNS - len(part))
            self.tree.insert("", "end", values=[start + 1] + cells)

    def to_clipboard(self):
        text = "\n".join(f"{v:.6f}" for v in self.vector)
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()

    def quit(self):
        self.server.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    try:
        Object2(root)
    except OSError:
        print("Object2 вже запущений")
        root.destroy()
    else:
        root.mainloop()
