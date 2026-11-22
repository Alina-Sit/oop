import tkinter as tk
from tkinter import ttk


class MyTable:
    def __init__(self, parent, columns, title="Таблиця", on_select=None, on_delete=None, on_close=None):
        self._on_select = on_select
        self._on_delete = on_delete
        self._on_close = on_close
        self._silent = False

        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry("460x320")
        self.window.transient(parent)
        self.window.protocol("WM_DELETE_WINDOW", self.hide)

        self.tree = ttk.Treeview(
            self.window, columns=[c[0] for c in columns], show="headings", selectmode="browse"
        )
        for key, heading, width in columns:
            self.tree.heading(key, text=heading)
            self.tree.column(key, width=width, anchor="center")
        scroll = ttk.Scrollbar(self.window, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)

        bottom = ttk.Frame(self.window)
        bottom.pack(side="bottom", fill="x", padx=6, pady=6)
        ttk.Button(bottom, text="Видалити вибраний", command=self._delete_clicked).pack(side="left")

        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="left", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self._selected)
        self.tree.bind("<Delete>", lambda e: self._delete_clicked())
        self.window.withdraw()

    def is_open(self):
        return self.window.state() != "withdrawn"

    def show(self):
        self.window.deiconify()
        self.window.lift()

    def hide(self):
        self.window.withdraw()
        if self._on_close:
            self._on_close()

    def destroy(self):
        self.window.destroy()

    def set_rows(self, rows):
        self._silent = True
        try:
            self.tree.delete(*self.tree.get_children())
            for index, row in enumerate(rows):
                self.tree.insert("", "end", iid=str(index), values=row)
        finally:
            self._silent = False

    def select_row(self, index):
        self._silent = True
        try:
            if index is None:
                self.tree.selection_remove(self.tree.selection())
            else:
                self.tree.selection_set(str(index))
                self.tree.see(str(index))
        finally:
            self._silent = False

    def selected_index(self):
        selection = self.tree.selection()
        return int(selection[0]) if selection else None

    def _selected(self, event):
        if self._silent:
            return
        if self._on_select:
            self._on_select(self.selected_index())

    def _delete_clicked(self):
        index = self.selected_index()
        if index is not None and self._on_delete:
            self._on_delete(index)
