import tkinter as tk
from tkinter import ttk, messagebox
from db_connection import get_connection, get_tokens, get_product_types

def open_cabinet_form(parent, cabinet_id=None, refresh_callback=None):
    win = tk.Toplevel(parent)
    win.title("WareHouse — Редактирование кабинета" if cabinet_id else "WareHouse — Новый кабинет")
    win.geometry("550x450")
    win.configure(bg="#FFFFFF")

    fields = {
        "cabinet_name": tk.StringVar(),
        "token_id": tk.StringVar(),
        "type_id": tk.StringVar(),
        "warehouse_id": tk.StringVar()
    }

    if cabinet_id:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT cabinet_name, token_id, type_id, warehouse_id FROM cabinets WHERE cabinet_id = %s", (cabinet_id,))
        data = cur.fetchone()
        if data:
            fields["cabinet_name"].set(data[0] or "")
            fields["token_id"].set(str(data[1]) if data[1] else "")
            fields["type_id"].set(str(data[2]) if data[2] else "")
            fields["warehouse_id"].set(str(data[3]) if data[3] else "")
        cur.close()
        conn.close()

    tk.Label(win, text="Наименование", font=("Inter", 10), bg="#FFFFFF", fg="black").grid(row=0, column=0, sticky="w", padx=20, pady=10)
    ttk.Entry(win, textvariable=fields["cabinet_name"], width=40, font=("Inter", 10)).grid(row=0, column=1, padx=20, pady=10)

    tokens = get_tokens()
    token_dict = {str(t[0]): t[1] for t in tokens}
    tk.Label(win, text="Токен", font=("Inter", 10), bg="#FFFFFF", fg="black").grid(row=1, column=0, sticky="w", padx=20, pady=10)
    ttk.Combobox(win, textvariable=fields["token_id"], values=list(token_dict.keys()), state="readonly", font=("Inter", 10), width=38).grid(row=1, column=1, padx=20, pady=10)

    types = get_product_types()
    type_dict = {str(t[0]): t[1] for t in types}
    tk.Label(win, text="Тип продукции", font=("Inter", 10), bg="#FFFFFF", fg="black").grid(row=2, column=0, sticky="w", padx=20, pady=10)
    ttk.Combobox(win, textvariable=fields["type_id"], values=list(type_dict.keys()), state="readonly", font=("Inter", 10), width=38).grid(row=2, column=1, padx=20, pady=10)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT warehouse_id, warehouse_name FROM warehouses ORDER BY warehouse_id;")
    wh_data = cur.fetchall()
    wh_dict = {str(w[0]): w[1] for w in wh_data}
    cur.close()
    conn.close()

    tk.Label(win, text="Склад", font=("Inter", 10), bg="#FFFFFF", fg="black").grid(row=3, column=0, sticky="w", padx=20, pady=10)
    ttk.Combobox(win, textvariable=fields["warehouse_id"], values=list(wh_dict.keys()), state="readonly", font=("Inter", 10), width=38).grid(row=3, column=1, padx=20, pady=10)

    def save():
        try:
            if not fields["cabinet_name"].get():
                messagebox.showwarning("Внимание", "Заполните наименование кабинета!")
                return

            token_id = int(fields["token_id"].get()) if fields["token_id"].get() else None
            type_id = int(fields["type_id"].get()) if fields["type_id"].get() else None
            warehouse_id = int(fields["warehouse_id"].get()) if fields["warehouse_id"].get() else None

            conn = get_connection()
            cur = conn.cursor()

            if cabinet_id:
                cur.execute("""
                    UPDATE cabinets SET cabinet_name=%s, token_id=%s, type_id=%s, warehouse_id=%s
                    WHERE cabinet_id=%s
                """, (fields["cabinet_name"].get(), token_id, type_id, warehouse_id, cabinet_id))
            else:
                cur.execute("""
                    INSERT INTO cabinets (cabinet_name, token_id, type_id, warehouse_id)
                    VALUES (%s, %s, %s, %s)
                """, (fields["cabinet_name"].get(), token_id, type_id, warehouse_id))

            conn.commit()
            cur.close()
            conn.close()

            messagebox.showinfo("Успех", "Кабинет сохранён.")
            if refresh_callback:
                refresh_callback()
            win.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка БД", f"Не удалось сохранить: {e}")

    btn_save = tk.Label(win, text="Сохранить", font=("Inter", 12, "bold"), bg="#EEEEEE", fg="black", padx=20, pady=10, cursor="hand2", relief="solid", bd=1)
    btn_save.bind("<Button-1>", lambda e: save())
    btn_save.grid(row=4, column=0, columnspan=2, pady=30)