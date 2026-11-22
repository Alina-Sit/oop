import tkinter as tk
from tkinter import messagebox

from editor import MyEditor, SHAPES
from toolbar import Toolbar

editor = MyEditor()


class EditorWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("OOP_Lab4")
        self._build_menu()
        self._build_toolbar()
        self._build_canvas()
        self.select_type(editor.current_key)

    def _build_menu(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Новий", command=self.on_new)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.root.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)

        objects_menu = tk.Menu(menubar, tearoff=0, postcommand=self.on_init_menu_popup)
        self.type_var = tk.StringVar(value=editor.current_key)
        for key, name, _ in SHAPES:
            objects_menu.add_radiobutton(
                label=name,
                variable=self.type_var,
                value=key,
                command=self.on_menu_type_change,
            )
        menubar.add_cascade(label="Об'єкти", menu=objects_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Про програму", command=self.on_about)
        menubar.add_cascade(label="Довідка", menu=help_menu)

        self.root.config(menu=menubar)

    def _build_toolbar(self):
        items = [(key, name) for key, name, _ in SHAPES]
        self.toolbar = Toolbar(self.root, items, self.select_type)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

    def _build_canvas(self):
        self.canvas = tk.Canvas(self.root, width=700, height=500, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

    def select_type(self, key):
        editor.set_type(key)
        self.type_var.set(key)
        self.toolbar.set_active(key)

    def on_menu_type_change(self):
        self.select_type(self.type_var.get())

    def on_init_menu_popup(self):
        self.type_var.set(editor.current_key)

    def on_new(self):
        editor.clear()
        self.canvas.delete("all")

    def on_about(self):
        messagebox.showinfo(
            "Про програму",
            "Лабораторна робота №4\nГрафічний редактор об'єктів\nВаріант 27",
        )

    def on_mouse_down(self, event):
        if not editor.on_lbdown(event.x, event.y):
            messagebox.showwarning("Увага", "Масив об'єктів переповнено")

    def on_mouse_move(self, event):
        editor.on_mouse_move(self.canvas, event.x, event.y)

    def on_mouse_up(self, event):
        editor.on_lbup(self.canvas, event.x, event.y)


if __name__ == "__main__":
    root = tk.Tk()
    window = EditorWindow(root)
    root.mainloop()
