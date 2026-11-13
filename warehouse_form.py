import tkinter as tk
from tkinter import ttk, messagebox
from db_connection import get_connection, get_tokens

def open_warehouse_form(parent, warehouse_id=None, refresh_callback=None):
    win = tk.Toplevel(parent)
    win.title("WareHouse — Редактирование склада" if warehouse_id else "WareHouse — Новый склад")
    win.geometry("550x600")
    win.configure(bg="#FFFFFF")

    fields = {
        "warehouse_name": tk.StringVar(),
        "owner_name": tk.StringVar(),
        "owner_inn": tk.StringVar(),
        "owner_phone": tk.StringVar(),
        "owner_email": tk.StringVar(),
        "owner_address": tk.StringVar(),
        "delivery_method": tk.StringVar(),
        "token_id": tk.StringVar()
    }

    if warehouse_id:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT w.warehouse_name, o.full_name, o.inn, o.phone, o.email, o.address, w.delivery_method, w.token_id
            FROM warehouses w
            LEFT JOIN owners o ON w.owner_id = o.owner_id
            WHERE w.warehouse_id = %s
        """, (warehouse_id,))
        data = cur.fetchone()
        if data:
            fields["warehouse_name"].set(data[0] or "")
            fields["owner_name"].set(data[1] or "")
            fields["owner_inn"].set(data[2] or "")
            fields["owner_phone"].set(data[3] or "")
            fields["owner_email"].set(data[4] or "")
            fields["owner_address"].set(data[5] or "")
            fields["delivery_method"].set(data[6] or "")
            fields["token_id"].set(str(data[7]) if data[7] else "")
        cur.close()
        conn.close()

    labels = [
        ("Название склада", "warehouse_name"),
        ("ФИО Владельца", "owner_name"),
        ("ИНН", "owner_inn"),
        ("Телефон", "owner_phone"),
        ("Email", "owner_email"),
        ("Адрес", "owner_address"),
        ("Способ доставки", "delivery_method"),
    ]

    for i, (label_text, key) in enumerate(labels):
        tk.Label(win, text=label_text, font=("Inter", 10), bg="#FFFFFF", fg="black").grid(row=i, column=0, sticky="w", padx=20, pady=5)
        entry = ttk.Entry(win, textvariable=fields[key], width=40, font=("Inter", 10))
        entry.grid(row=i, column=1, padx=20, pady=5)

    tk.Label(win, text="Токен", font=("Inter", 10), bg="#FFFFFF", fg="black").grid(row=len(labels), column=0, sticky="w", padx=20, pady=5)

    tokens = get_tokens()
    token_dict = {str(t[0]): t[1] for t in tokens}
    token_combo = ttk.Combobox(win, textvariable=fields["token_id"], values=list(token_dict.keys()), state="readonly", font=("Inter", 10), width=38)
    token_combo.grid(row=len(labels), column=1, padx=20, pady=5)

    def save():
        try:
            if not fields["warehouse_name"].get() or not fields["delivery_method"].get():
                messagebox.showwarning("Внимание", "Заполните название склада и способ доставки!")
                return

            conn = get_connection()
            cur = conn.cursor()

            owner_name = fields["owner_name"].get()
            owner_inn = fields["owner_inn"].get()
            owner_id = None

            if owner_inn:
                cur.execute("SELECT owner_id FROM owners WHERE inn = %s", (owner_inn,))
                res = cur.fetchone()
                if res:
                    owner_id = res[0]
                    cur.execute("""
                        UPDATE owners SET full_name=%s, phone=%s, email=%s, address=%s WHERE owner_id=%s
                    """, (owner_name, fields["owner_phone"].get(), fields["owner_email"].get(), fields["owner_address"].get(), owner_id))
                else:
                    cur.execute("""
                        INSERT INTO owners (full_name, email, phone, address, inn)
                        VALUES (%s, %s, %s, %s, %s) RETURNING owner_id
                    """, (owner_name, fields["owner_email"].get(), fields["owner_phone"].get(), fields["owner_address"].get(), owner_inn))
                    owner_id = cur.fetchone()[0]

            token_id = int(fields["token_id"].get()) if fields["token_id"].get() else None

            if warehouse_id:
                cur.execute("""
                    UPDATE warehouses SET warehouse_name=%s, owner_id=%s, token_id=%s, delivery_method=%s
                    WHERE warehouse_id=%s
                """, (fields["warehouse_name"].get(), owner_id, token_id, fields["delivery_method"].get(), warehouse_id))
            else:
                cur.execute("""
                    INSERT INTO warehouses (warehouse_name, owner_id, token_id, delivery_method)
                    VALUES (%s, %s, %s, %s)
                """, (fields["warehouse_name"].get(), owner_id, token_id, fields["delivery_method"].get()))

            conn.commit()
            cur.close()
            conn.close()

            messagebox.showinfo("Успех", "Склад сохранён.")
            if refresh_callback:
                refresh_callback()
            win.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка БД", f"Не удалось сохранить: {e}")

    btn_save = tk.Label(win, text="Сохранить", font=("Inter", 12, "bold"), bg="#EEEEEE", fg="black", padx=20, pady=10, cursor="hand2", relief="solid", bd=1)
    btn_save.bind("<Button-1>", lambda e: save())
    btn_save.grid(row=len(labels)+1, column=0, columnspan=2, pady=30)