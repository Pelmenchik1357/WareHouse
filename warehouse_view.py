import tkinter as tk
from tkinter import ttk
from db_connection import get_warehouses
from warehouse_form import open_warehouse_form

def open_warehouse_list(parent):
    win = tk.Toplevel(parent)
    win.title("WareHouse — Склады")
    win.geometry("900x600")
    win.configure(bg="#EEEEEE")

    header_frame = tk.Frame(win, bg="#EEEEEE")
    header_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(header_frame, text="Склады", font=("Inter", 16, "bold"), bg="#EEEEEE", fg="black").pack(side="left")

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

        warehouses = get_warehouses(sort_var.get())
        for w in warehouses:
            card = tk.Frame(scroll_frame, bg="white", padx=10, pady=10, relief="groove", bd=1)
            card.pack(fill="x", pady=5, padx=10)

            tk.Label(card, text=f"#{w[0]} {w[1]}", font=("Inter", 12, "bold"), bg="white", fg="black", anchor="w").pack(fill="x")
            tk.Label(card, text=f"Владелец: {w[3]}, ИНН: {w[4]}, Адрес: {w[5]}", font=("Inter", 10), bg="white", fg="black", anchor="w").pack(fill="x")

            status = "активен" if w[6] else "неактивен"
            tk.Label(card, text=f"Статус подключения: {status}", font=("Inter", 10), fg="#00B3FF", bg="white", anchor="w").pack(fill="x")

            card.bind("<Double-Button-1>", lambda e, wid=w[0]: open_warehouse_form(win, wid, refresh_list))

    sort_combo.bind("<<ComboboxSelected>>", refresh_list)
    refresh_list()

    btn_frame = tk.Frame(win, bg="#EEEEEE")
    btn_frame.pack(fill="x", padx=10, pady=10)

    btn_add = tk.Label(btn_frame, text="Добавить склад", font=("Inter", 10), bg="#EEEEEE", fg="black", padx=10, pady=5, cursor="hand2", relief="solid", bd=1)
    btn_add.bind("<Button-1>", lambda e: open_warehouse_form(win, None, refresh_list))
    btn_add.pack(side="left")

    btn_back = tk.Label(btn_frame, text="Назад", font=("Inter", 10), bg="#EEEEEE", fg="black", padx=10, pady=5, cursor="hand2", relief="solid", bd=1)
    btn_back.bind("<Button-1>", lambda e: win.destroy())
    btn_back.pack(side="right")