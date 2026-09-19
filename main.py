import tkinter as tk
from tkinter import ttk
from module1 import show_work1
from module2 import show_work2


def handle_work1():
    value = show_work1(root)

    if value is not None:
        message_var.set(value)


def handle_work2():
    value = show_work2(root)

    if value is not None:
        message_var.set(value)


root = tk.Tk()
root.title("lab1")
root.geometry("600x380")

style = ttk.Style()
style.theme_use("clam")

menu_bar = tk.Menu(root)

actions_menu = tk.Menu(menu_bar, tearoff=0)
actions_menu.add_command(label="Робота1", command=handle_work1)
actions_menu.add_command(label="Робота2", command=handle_work2)
menu_bar.add_cascade(label="Дії", menu=actions_menu)

root.config(menu=menu_bar)

message_var = tk.StringVar()
ttk.Label(root, textvariable=message_var, font=("Arial", 14, "bold")).pack(pady=170)

root.mainloop()