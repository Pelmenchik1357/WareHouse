import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from db_connection import get_cabinets
from cabinet_form import open_cabinet_form

def open_cabinet_list(parent):
    win = tk.Toplevel(parent)
    win.title("WareHouse — Кабинеты")
    win.geometry("900x600")
    win.configure(bg="#EEEEEE")

    header_frame = tk.Frame(win, bg="#EEEEEE")
    header_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(header_frame, text="Кабинеты", font=("Inter", 16, "bold"), bg="#EEEEEE", fg="black").pack(side="left")

    sort_var = tk.StringVar(value="default")
    sort_combo = ttk.Combobox(header_frame, textvariable=sort_var, values=["default", "name_asc", "name_desc"], state="readonly", width=15)
    sort_combo.pack(side="right")

    canvas = tk.Canvas(win, bg="#EEEEEE")
    scrollbar = ttk.Scrollbar(win, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#EEEEEE")

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def refresh_list(*args):
        for widget in scroll_frame.winfo_children():
            widget.destroy()

        cabinets = get_cabinets(sort_var.get())

        try:
            icon_img = Image.open("images/cabinet.png").resize((40, 40), Image.Resampling.LANCZOS)
            icon = ImageTk.PhotoImage(icon_img)
        except Exception:
            icon = None

        for i, c in enumerate(cabinets):
            row = i // 3
            col = i % 3
            card = tk.Frame(scroll_frame, bg="white", padx=10, pady=10, relief="groove", bd=1)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            if icon:
                icon_label = tk.Label(card, image=icon, bg="white")
                icon_label.image = icon
                icon_label.pack(pady=5)

            tk.Label(card, text=f"#{c[0]} {c[1]}", font=("Inter", 12, "bold"), bg="white", fg="black").pack()

            status = "активен" if c[2] else "неактивен"
            tk.Label(card, text=f"Статус токена: {status}", font=("Inter", 10), fg="#00B3FF", bg="white").pack()
            tk.Label(card, text=f"Создан: {c[3]}", font=("Inter", 9), bg="white", fg="black").pack()
            tk.Label(card, text=f"Истекает: {c[4]}", font=("Inter", 9), bg="white", fg="black").pack()
            tk.Label(card, text=f"Тип: {c[5]}", font=("Inter", 10), bg="white", fg="black").pack()

            card.bind("<Double-Button-1>", lambda e, cid=c[0]: open_cabinet_form(win, cid, refresh_list))

    sort_combo.bind("<<ComboboxSelected>>", refresh_list)
    refresh_list()

    btn_frame = tk.Frame(win, bg="#EEEEEE")
    btn_frame.pack(fill="x", padx=10, pady=10)

    btn_add = tk.Label(btn_frame, text="Добавить кабинет", font=("Inter", 10), bg="#EEEEEE", fg="black", padx=10, pady=5, cursor="hand2", relief="solid", bd=1)
    btn_add.bind("<Button-1>", lambda e: open_cabinet_form(win, None, refresh_list))
    btn_add.pack(side="left")

    btn_back = tk.Label(btn_frame, text="Назад", font=("Inter", 10), bg="#EEEEEE", fg="black", padx=10, pady=5, cursor="hand2", relief="solid", bd=1)
    btn_back.bind("<Button-1>", lambda e: win.destroy())
    btn_back.pack(side="right")