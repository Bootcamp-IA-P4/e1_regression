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
        """Guarda una NUEVA predicción."""
        if self.id:
            log.warning(f"Intento de actualizar Prediction ID {self.id}. Esta operación no está soportada.")
            return self

        if not self.property_id:
            raise ValueError("Se requiere 'property_id' para guardar una Prediction.")

        data_to_save = {
            'property_id': self.property_id,
            'predicted_value': self.predicted_value,
            'actual_value': self.actual_value
        }
        
        # Quitar 'actual_value' si es None para depender del default NULL de la tabla
        if data_to_save['actual_value'] is None:
            del data_to_save['actual_value']

        try:
            self.id = insert_and_get_id('predictions', data_to_save)
            log.info(f"Nueva predicción guardada con ID: {self.id}")
            return self
        except Exception as e:
            log.error(f"Error al guardar predicción: {e}")
            raise

    @classmethod
    def find_by_id(cls, prediction_id):
        """Busca una predicción por su ID."""
        query = "SELECT * FROM predictions WHERE id = %s"
        row = execute_query(query, (prediction_id,), fetch_one=True)
        return cls._from_db_row(row) if row else None

    @classmethod
    def get_recent_with_property(cls, limit=10):
        """Obtiene predicciones recientes con datos de la propiedad asociada."""
        query = """
        SELECT 
            p.id, p.property_id, p.predicted_value, p.actual_value, 
            p.created_at as prediction_created_at,
            pr.calidad_general AS CalidadGeneral, 
            pr.metros_habitables AS MetrosHabitables,
            pr.coches_garaje AS CochesGaraje,
            pr.banos_completos AS BañosCompletos,
            pr.total_habitaciones_sobre_suelo AS TotalHabitacionesSobreSuelo,
            pr.ano_construccion AS AñoConstrucción,
            pr.vecindario AS Vecindario
        FROM predictions p
        JOIN properties pr ON p.property_id = pr.id
        ORDER BY p.created_at DESC
        LIMIT %s
        """
        results = execute_query(query, (limit,), fetch_all=True)
        return results  # Devolvemos directamente el diccionario para usar en templates

    @classmethod
    def create_for_property(cls, property_instance, predicted_value, actual_value=None):
        """Crea una predicción para una propiedad existente."""
        if not property_instance.id:
            raise ValueError("La propiedad debe estar guardada (tener ID) antes de crear una predicción")
        
        prediction = cls(
            property_id=property_instance.id,
            predicted_value=predicted_value,
            actual_value=actual_value
        )
        return prediction.save()

    @classmethod
    def create_from_data(cls, property_data: dict, prediction_data: dict):
        """Crea una propiedad y una predicción asociada en una sola operación."""
        from .property import Property  # Importación local para evitar circular imports
        
        # Crear y guardar la propiedad
        property_instance = Property(**property_data)
        property_instance.save()
        
        # Crear y guardar la predicción
        prediction = cls(
            property_id=property_instance.id,
            predicted_value=prediction_data.get('predicted_value'),
            actual_value=prediction_data.get('actual_value')
        )
        return prediction.save()