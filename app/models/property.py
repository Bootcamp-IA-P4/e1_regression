# app/models/property.py
from app.utils.db_utils import execute_query, insert_and_get_id
from flask import current_app
import logging

log = logging.getLogger(__name__)

class Property:
    """Modelo ORM-like para la tabla 'properties'."""

    # Nombres de campo deben coincidir con columnas de la tabla (o mapearse)
    def __init__(self, id=None, med_income=None, house_age=None, ave_rooms=None,
                 ave_bedrooms=None, population=None, ave_occupancy=None,
                 latitude=None, longitude=None, median_value=None, created_at=None):
        self.id = id
        self.med_income = med_income
        self.house_age = house_age
        self.ave_rooms = ave_rooms
        self.ave_bedrooms = ave_bedrooms
        self.population = population
        self.ave_occupancy = ave_occupancy
        self.latitude = latitude
        self.longitude = longitude
        self.median_value = median_value # Permitir Nulo
        self.created_at = created_at # Establecido por la BD

    def to_dict(self, include_id=True):
        """Convierte el objeto a un diccionario."""
        data = {
            'med_income': self.med_income,
            'house_age': self.house_age,
            'ave_rooms': self.ave_rooms,
            'ave_bedrooms': self.ave_bedrooms,
            'population': self.population,
            'ave_occupancy': self.ave_occupancy,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'median_value': self.median_value
            # No incluimos created_at ya que es manejado por la BD
        }
        if include_id and self.id:
            data['id'] = self.id
        if self.created_at: # Añadir si está presente
             data['created_at'] = self.created_at
        return data

    @classmethod
    def _from_db_row(cls, row):
        """Crea una instancia de Property desde un diccionario (fila de BD)."""
        if not row:
            return None
        # Asume que row es un diccionario (gracias a DictCursor)
        return cls(**row) # Desempaqueta el diccionario en los argumentos del constructor

    def save(self):
        """Guarda (inserta o actualiza) la propiedad en la base de datos."""
        data_to_save = self.to_dict(include_id=False) # Excluye ID para INSERT/UPDATE data

        # Remover valores None explícitos si la columna no lo permite o tiene DEFAULT
        # (Excepto median_value que sí puede ser NULL)
        data_to_save = {k: v for k, v in data_to_save.items() if v is not None or k == 'median_value'}
        # Excluir created_at porque lo maneja la BD
        data_to_save.pop('created_at', None)

        try:
            if self.id:
                # Actualizar registro existente
                if not data_to_save: # Nada que actualizar
                    log.warning(f"Intento de actualizar Property ID {self.id} sin datos.")
                    return self

                set_clause = ', '.join([f"`{k}`=%s" for k in data_to_save.keys()])
                query = f"UPDATE `properties` SET {set_clause} WHERE `id`=%s"
                params = tuple(data_to_save.values()) + (self.id,)
                affected_rows = execute_query(query, params)
                log.info(f"Property ID {self.id} actualizada. Filas afectadas: {affected_rows}")
            else:
                # Insertar nuevo registro
                if not data_to_save:
                     raise ValueError("No hay datos válidos para insertar en Property.")
                last_id = insert_and_get_id('properties', data_to_save)
                if last_id:
                    self.id = last_id
                    log.info(f"Nueva Property creada con ID: {self.id}")
                else:
                    # Esto no debería ocurrir si insert_and_get_id lanza excepción en error
                    log.error("insert_and_get_id devolvió None/0 sin lanzar excepción.")
                    return None
            return self # Devuelve la instancia (con ID si fue inserción)
        except Exception as e:
            log.exception(f"Error al guardar Property (ID: {self.id}): {e}")
            # Considera cómo manejar el error (¿relanzar? ¿devolver None?)
            raise # Relanzar es a menudo la mejor opción para que la capa superior decida

    @classmethod
    def find_by_id(cls, property_id):
        """Busca una propiedad por su ID."""
        query = "SELECT * FROM `properties` WHERE `id` = %s"
        try:
            result_row = execute_query(query, (property_id,), fetch_one=True)
            return cls._from_db_row(result_row)
        except Exception as e:
            log.exception(f"Error al buscar Property por ID {property_id}: {e}")
            return None # O considera relanzar

    @classmethod
    def find_all(cls, limit=100, offset=0):
        """Busca todas las propiedades con paginación opcional."""
        query = "SELECT * FROM `properties` ORDER BY `created_at` DESC LIMIT %s OFFSET %s"
        properties = []
        try:
            results = execute_query(query, (limit, offset), fetch_all=True)
            if results:
                properties = [cls._from_db_row(row) for row in results if row]
            return properties
        except Exception as e:
            log.exception(f"Error al buscar todas las Properties: {e}")
            return [] # Devuelve lista vacía en caso de error

    @classmethod
    def create(cls, **kwargs):
       """Método de conveniencia para crear y guardar una nueva propiedad."""
       # Filtra kwargs para asegurar que solo pasamos atributos válidos
       valid_args = {k: v for k, v in kwargs.items() if hasattr(cls, k) and k != 'id' and k != 'created_at'}
       instance = cls(**valid_args)
       return instance.save() # Llama al método save para insertar y obtener ID