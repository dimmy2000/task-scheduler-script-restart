import random
from tkinter import messagebox


def action():
    num = random.randint(0, 3)

    if num == 1:
        messagebox.showinfo(title='Info', message='Success')
        raise SystemExit(0)
    else:
        messagebox.showerror(title='Error', message='Fail')
        raise SystemExit(1)


if __name__ == "__main__":
    action()
