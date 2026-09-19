import tkinter as tk
from tkinter import ttk
from utils import create_dialog, close_dialog


def show_work2(parent):
    dialog = create_dialog(parent, "Робота2")
    result = [None]

    entry_var = tk.StringVar()
    entry = ttk.Entry(dialog, textvariable=entry_var, width=30)
    entry.pack(padx=16, pady=16)
    entry.focus_set()

    buttons = ttk.Frame(dialog)
    buttons.pack(pady=(0, 16))

    ttk.Button(buttons, text="Так", width=10, command=lambda: close_dialog(dialog, result, entry_var.get())).pack(side="left", padx=4)

    ttk.Button(buttons, text="Відміна", width=10, command=lambda: close_dialog(dialog, result, None)).pack(side="left", padx=4)

    dialog.wait_window()
    return result[0]