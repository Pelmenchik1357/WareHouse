import tkinter as tk
from PIL import Image, ImageTk
from warehouse_view import open_warehouse_list
from cabinet_view import open_cabinet_list

def create_main_window():
    root = tk.Tk()
    root.title("WareHouse — Главное меню")
    root.geometry("500x450")
    root.configure(bg="#FFFFFF")

    try:
        root.iconbitmap("images/logo.ico")
    except Exception:
        pass

    try:
        img = Image.open("images/logo.png")
        img = img.resize((150, 150), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(img)
        logo_label = tk.Label(root, image=logo, bg="#FFFFFF")
        logo_label.image = logo
        logo_label.pack(pady=20)
    except Exception:
        tk.Label(root, text="WH", font=("Inter", 40, "bold"), bg="#FFFFFF", fg="black").pack(pady=20)

    tk.Label(root, text="Система управления складами и кабинетами", font=("Inter", 12), bg="#FFFFFF", fg="black").pack(pady=10)

    def create_btn(text, command):
        btn = tk.Label(root, text=text, font=("Inter", 12), bg="#EEEEEE", fg="black",
                       width=20, height=2, cursor="hand2", relief="solid", bd=1)
        btn.bind("<Button-1>", lambda e: command())
        return btn

    create_btn("Склады", lambda: open_warehouse_list(root)).pack(pady=10)
    create_btn("Кабинеты", lambda: open_cabinet_list(root)).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_main_window()