from app import mysql

def execute_query(query, params=None, fetch=True):
    """Ejecuta una consulta SQL y devuelve los resultados."""
    cursor = mysql.connection.cursor()
    cursor.execute(query, params or ())
    
    result = None
    if fetch:
        result = cursor.fetchall()
    else:
        mysql.connection.commit()
    
    cursor.close()
    return result

def insert_and_get_id(table, data):
    """Inserta datos en una tabla y devuelve el ID generado."""
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    values = tuple(data.values())
    
    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    
    cursor = mysql.connection.cursor()
    cursor.execute(query, values)
    last_id = cursor.lastrowid
    mysql.connection.commit()
    cursor.close()
    
    return last_id