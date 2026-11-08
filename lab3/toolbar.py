import tkinter as tk

from icons import make_icon
from tooltip import Tooltip


class Toolbar(tk.Frame):
    def __init__(self, parent, items, on_select):
        super().__init__(parent, bd=1, relief=tk.RAISED)
        self.on_select = on_select
        self.buttons = {}
        self.icons = {}

        for key, hint in items:
            icon = make_icon(key)
            self.icons[key] = icon
            button = tk.Button(
                self, image=icon, relief=tk.RAISED,
                command=lambda k=key: self.on_select(k)
            )
            button.pack(side=tk.LEFT, padx=2, pady=2)
            Tooltip(button, hint)
            self.buttons[key] = button

    def set_active(self, key):
        for k, button in self.buttons.items():
            button.config(relief=tk.SUNKEN if k == key else tk.RAISED)