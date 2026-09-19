import tkinter as tk
from tkinter import ttk
from lab1.utils import create_dialog, close_dialog

GROUPS = [
    "ІП-31", "ІП-32", "ІП-33",
    "ІО-31", "ІО-32",
    "СП-31", "СП-32",
    "ТР-31", "ТР-32",
]


def show_work1(parent):
    dialog = create_dialog(parent, "Робота1")
    result = [None]

    listbox = tk.Listbox(dialog, height=8, width=20, exportselection=False)
    for group in GROUPS:
        listbox.insert(tk.END, group)
    listbox.select_set(0)
    listbox.pack(padx=16, pady=(16, 8))

    buttons = ttk.Frame(dialog)
    buttons.pack(pady=(0, 16))

    def on_ok():
        selection = listbox.curselection()
        value = listbox.get(selection[0]) if selection else None
        close_dialog(dialog, result, value)

    ttk.Button(buttons, text="Так", width=10, command=on_ok).pack(side="left", padx=4)

    ttk.Button(buttons, text="Відміна", width=10, command=lambda: close_dialog(dialog, result, None)).pack(side="left", padx=4)

    dialog.wait_window()
    return result[0]