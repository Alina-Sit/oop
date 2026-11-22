import tkinter as tk
from tkinter import filedialog, messagebox

from editor import MyEditor
from my_table import MyTable
from toolbar import Toolbar

TABLE_COLUMNS = [
    ("n", "№", 40),
    ("type", "Тип", 140),
    ("x1", "x1", 55),
    ("y1", "y1", 55),
    ("x2", "x2", 55),
    ("y2", "y2", 55),
]


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.editor = MyEditor.instance()
        self.root.title("OOP_Lab5")

        self._build_menu()
        self._build_toolbar()
        self._build_canvas()
        self.table = MyTable(
            self.root, TABLE_COLUMNS, title="Таблиця об'єктів",
            on_select=self.editor.select, on_delete=self.editor.remove,
            on_close=self.on_table_closed,
        )
        self.editor.add_listener(self.on_editor_event)
        self.select_type(self.editor.current_key)
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

    def _build_menu(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Новий", command=self.on_new)
        file_menu.add_command(label="Відкрити...", command=self.on_open)
        file_menu.add_command(label="Зберегти як...", command=self.on_save)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.on_exit)
        menubar.add_cascade(label="Файл", menu=file_menu)

        objects_menu = tk.Menu(menubar, tearoff=0, postcommand=self.on_init_menu_popup)
        self.type_var = tk.StringVar(value=self.editor.current_key)
        for key, name in self.editor.type_names():
            objects_menu.add_radiobutton(
                label=name, variable=self.type_var, value=key,
                command=self.on_menu_type_change,
            )
        menubar.add_cascade(label="Об'єкти", menu=objects_menu)

        window_menu = tk.Menu(menubar, tearoff=0)
        self.table_var = tk.BooleanVar(value=False)
        window_menu.add_checkbutton(
            label="Таблиця об'єктів", variable=self.table_var, command=self.on_toggle_table
        )
        menubar.add_cascade(label="Вікно", menu=window_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Про програму", command=self.on_about)
        menubar.add_cascade(label="Довідка", menu=help_menu)

        self.root.config(menu=menubar)

    def _build_toolbar(self):
        self.toolbar = Toolbar(self.root, self.editor.type_names(), self.select_type)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

    def _build_canvas(self):
        self.canvas = tk.Canvas(self.root, width=700, height=500, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

    def select_type(self, key):
        self.editor.set_type(key)
        self.type_var.set(key)
        self.toolbar.set_active(key)

    def on_menu_type_change(self):
        self.select_type(self.type_var.get())

    def on_init_menu_popup(self):
        self.type_var.set(self.editor.current_key)

    def on_editor_event(self, event):
        self.editor.repaint(self.canvas)
        if event == "shapes":
            self.table.set_rows(self.editor.rows())
        self.table.select_row(self.editor.selected)

    def on_toggle_table(self):
        if self.table_var.get():
            self.table.show()
        else:
            self.table.hide()

    def on_table_closed(self):
        self.table_var.set(False)

    def on_new(self):
        self.editor.clear()

    def on_open(self):
        path = filedialog.askopenfilename(
            title="Відкрити файл об'єктів",
            filetypes=[("Текстові файли", "*.txt"), ("Усі файли", "*.*")],
        )
        if path:
            self.open_file(path)

    def on_save(self):
        path = filedialog.asksaveasfilename(
            title="Зберегти файл об'єктів", defaultextension=".txt",
            filetypes=[("Текстові файли", "*.txt")],
        )
        if path:
            self.save_file(path)

    def open_file(self, path):
        try:
            loaded, skipped = self.editor.load(path)
        except OSError as error:
            messagebox.showerror("Помилка", str(error))
            return None
        if skipped:
            messagebox.showwarning("Увага", f"Пропущено некоректних рядків: {skipped}")
        return loaded, skipped

    def save_file(self, path):
        try:
            return self.editor.save(path)
        except OSError as error:
            messagebox.showerror("Помилка", str(error))
            return None

    def on_about(self):
        messagebox.showinfo(
            "Про програму",
            "Лабораторна робота №5\nБагатовіконний графічний редактор\nВаріант 27",
        )

    def on_mouse_down(self, event):
        if not self.editor.on_lbdown(event.x, event.y):
            messagebox.showwarning("Увага", "Масив об'єктів переповнено")

    def on_mouse_move(self, event):
        self.editor.on_mouse_move(self.canvas, event.x, event.y)

    def on_mouse_up(self, event):
        self.editor.on_lbup(self.canvas, event.x, event.y)

    def on_exit(self):
        self.table.destroy()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    window = MainWindow(root)
    root.mainloop()
