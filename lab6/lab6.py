import os
import queue
import subprocess
import sys
import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk

from ipc import PORT_OBJECT2, PORT_OBJECT3, is_alive, send

FOLDER = os.path.dirname(os.path.abspath(__file__))
PROGRAMS = {
    "Object2": (PORT_OBJECT2, "object2.py"),
    "Object3": (PORT_OBJECT3, "object3.py"),
}


def ensure_running(name, log):
    port, script = PROGRAMS[name]
    if is_alive(port):
        log(f"{name} вже запущений — використовую його")
        return
    log(f"Запускаю {name}...")
    subprocess.Popen([sys.executable, os.path.join(FOLDER, script)], cwd=FOLDER)
    for _ in range(100):
        if is_alive(port):
            log(f"{name} готовий")
            return
        time.sleep(0.1)
    raise RuntimeError(f"{name} не відповідає")


def layout(sw, sh):
    obj2_w = min(460, sw // 2 - 40)
    obj2_h = min(400, sh - 340)
    obj3_x = max(500, 40 + obj2_w)
    obj3_w = max(300, min(640, sw - obj3_x - 20))
    obj3_h = min(500, sh - 100)
    return (
        f"{obj2_w}x{obj2_h}+20+300",
        f"{obj3_w}x{obj3_h}+{obj3_x}+20",
    )


class Lab6App:
    def __init__(self, root):
        self.root = root
        root.title("Lab6 — менеджер")
        root.geometry("420x230+20+20")
        self.status = tk.StringVar(value="Готовий до роботи")
        self.messages = queue.Queue()
        self.busy = False

        menubar = tk.Menu(root)
        work = tk.Menu(menubar, tearoff=0)
        work.add_command(label="Виконати завдання...", command=self.open_dialog)
        work.add_separator()
        work.add_command(label="Вихід", command=self.on_exit)
        menubar.add_cascade(label="Робота", menu=work)
        root.config(menu=menubar)

        ttk.Label(root, text="Варіант 3: вектор → буфер обміну → графік",
                  font=("Arial", 11, "bold")).pack(pady=(18, 6))
        ttk.Label(root, textvariable=self.status, wraplength=380, justify="center").pack(pady=10)
        root.protocol("WM_DELETE_WINDOW", self.on_exit)
        root.after(100, self.drain)

    def drain(self):
        try:
            while True:
                self.status.set(self.messages.get_nowait())
        except queue.Empty:
            pass
        self.root.after(100, self.drain)

    def open_dialog(self):
        if self.busy:
            return
        dialog = tk.Toplevel(self.root)
        dialog.title("Параметри")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        fields = {}
        for row, (label, default) in enumerate((("n", "20"), ("Min", "-10"), ("Max", "10"))):
            ttk.Label(dialog, text=label + ":").grid(row=row, column=0, padx=10, pady=6, sticky="e")
            entry = ttk.Entry(dialog, width=14)
            entry.insert(0, default)
            entry.grid(row=row, column=1, padx=10, pady=6)
            fields[label] = entry

        def accept():
            try:
                n = int(fields["n"].get())
                low = float(fields["Min"].get().replace(",", "."))
                high = float(fields["Max"].get().replace(",", "."))
            except ValueError:
                messagebox.showerror("Помилка", "Введіть коректні числа", parent=dialog)
                return
            if not 1 <= n <= 1000:
                messagebox.showerror("Помилка", "n має бути від 1 до 1000", parent=dialog)
                return
            if low > high:
                messagebox.showerror("Помилка", "Min не може бути більшим за Max", parent=dialog)
                return
            dialog.destroy()
            self.run(n, low, high)

        buttons = ttk.Frame(dialog)
        buttons.grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(buttons, text="Так", command=accept).pack(side="left", padx=6)
        ttk.Button(buttons, text="Відміна", command=dialog.destroy).pack(side="left", padx=6)
        dialog.bind("<Return>", lambda e: accept())

    def run(self, n, low, high):
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        geo2, geo3 = layout(sw, sh)
        self.busy = True
        threading.Thread(target=self.worker, args=(n, low, high, geo2, geo3), daemon=True).start()

    def worker(self, n, low, high, geo2, geo3):
        log = self.messages.put
        try:
            ensure_running("Object2", log)
            ensure_running("Object3", log)
            log("Надсилаю Object2 параметри...")
            reply = send(PORT_OBJECT2, {"cmd": "generate", "n": n, "min": low, "max": high, "geometry": geo2}, 5)
            if not reply.get("ok"):
                raise RuntimeError("Object2: " + reply.get("error", "помилка"))
            log(f"Object2 створив {reply['count']} чисел і поклав їх у буфер обміну")
            reply = send(PORT_OBJECT3, {"cmd": "plot", "geometry": geo3}, 5)
            if not reply.get("ok"):
                raise RuntimeError("Object3: " + reply.get("error", "помилка"))
            log(f"Готово: Object3 побудував графік ({reply['count']} точок)")
        except Exception as error:
            log(f"Помилка: {error}")
        finally:
            self.busy = False

    def on_exit(self):
        for port in (PORT_OBJECT2, PORT_OBJECT3):
            if is_alive(port):
                try:
                    send(port, {"cmd": "quit"}, 2)
                except OSError:
                    pass
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    Lab6App(root)
    root.mainloop()
