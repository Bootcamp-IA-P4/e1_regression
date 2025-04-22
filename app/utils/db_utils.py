# app/utils/db_utils.py
from app import mysql  # Importa la instancia mysql de app/__init__.py
from flask import current_app
import logging

log = logging.getLogger(__name__)

def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """
    Ejecuta una consulta SQL de forma segura.
    Utiliza el cursor configurado (ej. DictCursor).
    Maneja commit/rollback automáticamente para operaciones de escritura.
    """
    conn = mysql.connection
    cursor = conn.cursor() # Obtendrá DictCursor si está configurado
    result = None
    try:
        log.debug(f"Ejecutando Query: {query} con Params: {params}")
        cursor.execute(query, params or ())

        if fetch_one:
            result = cursor.fetchone()
            log.debug(f"Query Resultado (fetch_one): {result}")
        elif fetch_all:
            result = cursor.fetchall()
            log.debug(f"Query Resultado (fetch_all): {len(result) if result else 0} filas")
        else:
            # Operación de escritura (INSERT, UPDATE, DELETE)
            conn.commit()
            result = cursor.rowcount # Devuelve número de filas afectadas
            log.debug(f"Query (Escritura) completada. Filas afectadas: {result}")

    except Exception as e:
        conn.rollback() # Deshacer cambios en caso de error
        log.exception(f"Error en BD ejecutando query: {query} - Params: {params} - Error: {e}")
        raise # Relanzar para que la capa superior maneje el error
    finally:
        cursor.close()

    return result

def insert_and_get_id(table, data):
    """
    Inserta un diccionario de datos en una tabla y devuelve el ID generado.
    """
    if not data or not isinstance(data, dict):
        raise ValueError("Se requiere un diccionario de datos no vacío para insertar.")

    # Usar backticks `` para proteger nombres de tablas/columnas
    columns = ', '.join([f"`{k}`" for k in data.keys()])
    placeholders = ', '.join(['%s'] * len(data))
    values = tuple(data.values())

    query = f"INSERT INTO `{table}` ({columns}) VALUES ({placeholders})"

    conn = mysql.connection
    cursor = conn.cursor()
    last_id = None
    try:
        log.debug(f"Insertando en Tabla: {table} - Datos: {data}")
        cursor.execute(query, values)
        last_id = cursor.lastrowid
        conn.commit()
        log.info(f"Inserción exitosa en tabla '{table}'. Nuevo ID: {last_id}")
    except Exception as e:
        conn.rollback()
        log.exception(f"Error en BD insertando en '{table}': Datos: {data} - Error: {e}")
        raise
    finally:
        cursor.close()

    return last_id

# Podrías añadir más utilidades si lo ves necesario, por ejemplo:
# def update_record(table, data, where_clause, where_params): ...
# def delete_record(table, where_clause, where_params): ...