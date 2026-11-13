import psycopg2

DB_CONFIG = {
    "dbname": "warehouse_db",
    "user": "anna",
    "host": "localhost",
    "port": "5432"
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def get_warehouses(sort_mode="default"):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT w.warehouse_id, w.warehouse_name, w.delivery_method,
               o.full_name, o.inn, o.address,
               t.token_value, t.created_at, t.expires_at
        FROM warehouses w
        LEFT JOIN owners o ON w.owner_id = o.owner_id
        LEFT JOIN tokens t ON w.token_id = t.token_id
    """

    if sort_mode == "name_asc":
        query += " ORDER BY w.warehouse_name ASC;"
    elif sort_mode == "name_desc":
        query += " ORDER BY w.warehouse_name DESC;"
    else:
        query += " ORDER BY w.warehouse_id ASC;"

    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    conn.close()
    return result

def get_cabinets(sort_mode="default"):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT c.cabinet_id, c.cabinet_name,
               t.token_value, t.created_at, t.expires_at,
               pt.type_name,
               w.warehouse_name
        FROM cabinets c
        LEFT JOIN tokens t ON c.token_id = t.token_id
        LEFT JOIN product_types pt ON c.type_id = pt.type_id
        LEFT JOIN warehouses w ON c.warehouse_id = w.warehouse_id
    """

    if sort_mode == "name_asc":
        query += " ORDER BY c.cabinet_name ASC;"
    elif sort_mode == "name_desc":
        query += " ORDER BY c.cabinet_name DESC;"
    else:
        query += " ORDER BY c.cabinet_id ASC;"

    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    conn.close()
    return result

def get_tokens():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT token_id, token_value FROM tokens ORDER BY token_id;")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_product_types():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT type_id, type_name FROM product_types ORDER BY type_id;")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result