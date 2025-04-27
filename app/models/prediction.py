# app/models/prediction.py
from app.utils.db_utils import execute_query, insert_and_get_id
# Importa Property para referencias/validaciones si es necesario
from .property import Property
from flask import current_app
from datetime import datetime
import logging

log = logging.getLogger(__name__)

class Prediction:
    """Modelo ORM-like para la tabla 'predictions'."""

    def __init__(self, id=None, property_id=None, predicted_value=None,
                 actual_value=None, created_at=None):
        self.id = id
        self.property_id = property_id
        self.predicted_value = predicted_value
        self.actual_value = actual_value # Permitir Nulo
        self.created_at = created_at or datetime.now() # Puede ser de la BD o generado aquí

    def to_dict(self, include_id=True):
        """Convierte el objeto a un diccionario."""
        data = {
            'property_id': self.property_id,
            'predicted_value': self.predicted_value,
            'actual_value': self.actual_value,
            # No incluimos created_at ya que es manejado por la BD (o ya está en self.created_at)
        }
        if include_id and self.id:
             data['id'] = self.id
        if self.created_at:
             data['created_at'] = self.created_at # Añadir si está presente
        return data

    @classmethod
    def _from_db_row(cls, row):
        """Crea una instancia de Prediction desde un diccionario (fila de BD)."""
        if not row:
            return None
        return cls(**row)

    def save(self):
        """
        Guarda una NUEVA predicción. Actualizar predicciones generalmente no tiene sentido.
        """
        if self.id:
            log.warning(f"Intento de actualizar Prediction ID {self.id}. Esta operación no está soportada.")
            return self

        if not self.property_id:
             raise ValueError("Se requiere 'property_id' para guardar una Prediction.")

        # Validación de rango para evitar valores absurdos
        if self.predicted_value is not None:
            if self.predicted_value < 0 or self.predicted_value > 2_000_000:
                log.error(f"Predicción fuera de rango: {self.predicted_value}")
                raise ValueError(f"Predicción fuera de rango almacenable: {self.predicted_value}")

        data_to_save = {
            'property_id': self.property_id,
            'predicted_value': self.predicted_value,
            'actual_value': self.actual_value
        }
        if data_to_save['actual_value'] is None:
             data_to_save.pop('actual_value', None)

        try:
            last_id = insert_and_get_id('predictions', data_to_save)
            if last_id:
                self.id = last_id
                log.info(f"Nueva Prediction creada con ID: {self.id} para Property ID: {self.property_id}")
            else:
                 log.error("insert_and_get_id devolvió None/0 sin lanzar excepción para Prediction.")
                 return None
            return self
        except Exception as e:
            log.exception(f"Error al guardar Prediction para Property ID {self.property_id}: {e}")
            raise

    @classmethod
    def find_by_id(cls, prediction_id):
        """Busca una predicción por su ID."""
        query = "SELECT * FROM `predictions` WHERE `id` = %s"
        try:
            result_row = execute_query(query, (prediction_id,), fetch_one=True)
            return cls._from_db_row(result_row)
        except Exception as e:
            log.exception(f"Error al buscar Prediction por ID {prediction_id}: {e}")
            return None

    @classmethod
    def get_recent_with_property(cls, limit=10):
        """
        Obtiene las predicciones más recientes junto con los datos de la propiedad asociada.
        Devuelve una lista de diccionarios combinados directamente desde la BD.
        """
        query = """
            SELECT
                p.id AS prediction_id, p.property_id, p.predicted_value,
                p.actual_value, p.created_at AS prediction_created_at,
                pr.* -- Selecciona todas las columnas de properties
            FROM predictions p
            JOIN properties pr ON p.property_id = pr.id
            ORDER BY p.created_at DESC
            LIMIT %s
        """
        try:
            # execute_query con fetch_all=True y DictCursor devolverá lista de diccionarios
            results = execute_query(query, (limit,), fetch_all=True)
            log.debug(f"Obtenidas {len(results) if results else 0} predicciones recientes con propiedad.")
            return results if results else []
        except Exception as e:
            log.exception(f"Error al obtener predicciones recientes con propiedad: {e}")
            return []

    @classmethod
    def create_for_property(cls, property_instance, predicted_value, actual_value=None):
         """Crea y guarda una predicción para una instancia de Property existente."""
         if not property_instance or not property_instance.id:
             raise ValueError("Se requiere una instancia de Property válida y guardada (con ID).")

         prediction = cls(
             property_id=property_instance.id,
             predicted_value=predicted_value,
             actual_value=actual_value
         )
         return prediction.save()

    @classmethod
    def create_from_data(cls, property_data: dict, prediction_data: dict):
        """
        (Alternativa a create_and_save original)
        1. Crea y guarda la propiedad desde `property_data`.
        2. Crea y guarda la predicción desde `prediction_data`, usando el ID de la propiedad creada.

        Retorna: Tupla (saved_property, saved_prediction) o (None, None) en error.
        """
        saved_property = None
        saved_prediction = None
        try:
            # Crear y guardar propiedad
            saved_property = Property.create(**property_data) # Usa el classmethod de Property
            if not saved_property:
                log.error("Falló la creación/guardado de Property en create_from_data.")
                return None, None # Propiedad no se pudo guardar

            # Crear y guardar predicción
            prediction_instance = cls(
                property_id=saved_property.id,
                predicted_value=prediction_data.get('predicted_value'),
                actual_value=prediction_data.get('actual_value')
            )
            saved_prediction = prediction_instance.save()
            if not saved_prediction:
                 log.error(f"Falló el guardado de Prediction para Property ID {saved_property.id}")
                 # Considerar si deshacer la creación de la propiedad (Transacción?)
                 # Por ahora, la propiedad queda creada pero la predicción falló.
                 return saved_property, None # Devuelve la propiedad creada pero None para predicción

            return saved_property, saved_prediction

        except Exception as e:
            log.exception("Error durante Prediction.create_from_data", exc_info=True)
            # Devuelve lo que se haya podido crear (puede ser None, None)
            return saved_property, saved_prediction