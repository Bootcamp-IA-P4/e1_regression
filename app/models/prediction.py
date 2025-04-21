from app import mysql
from datetime import datetime

class Prediction:
    """Modelo para registrar predicciones hechas por el modelo ML."""
    
    def __init__(self, id=None, property_id=None, predicted_value=None, 
                 actual_value=None, created_at=None):
        self.id = id
        self.property_id = property_id
        self.predicted_value = predicted_value
        self.actual_value = actual_value
        self.created_at = created_at or datetime.now()
    
    def save(self):
        """Guarda la predicción en la base de datos."""
        cursor = mysql.connection.cursor()
        
        if self.id:
            # Actualizar registro existente
            cursor.execute('''
                UPDATE predictions 
                SET property_id=%s, predicted_value=%s, actual_value=%s
                WHERE id=%s
            ''', (
                self.property_id, self.predicted_value, self.actual_value, self.id
            ))
        else:
            # Insertar nuevo registro
            cursor.execute('''
                INSERT INTO predictions (
                    property_id, predicted_value, actual_value, created_at
                ) VALUES (%s, %s, %s, %s)
            ''', (
                self.property_id, self.predicted_value, self.actual_value, self.created_at
            ))
            self.id = cursor.lastrowid
        
        mysql.connection.commit()
        cursor.close()
        return self
    
    @staticmethod
    def get_recent(limit=10):
        """Obtiene las predicciones más recientes."""
        cursor = mysql.connection.cursor()
        cursor.execute('''
            SELECT p.id, p.property_id, p.predicted_value, p.actual_value, p.created_at,
                   pr.med_income, pr.house_age, pr.ave_rooms, pr.ave_bedrooms, 
                   pr.population, pr.ave_occupancy, pr.latitude, pr.longitude
            FROM predictions p
            JOIN properties pr ON p.property_id = pr.id
            ORDER BY p.created_at DESC
            LIMIT %s
        ''', (limit,))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'prediction': {
                    'id': row[0],
                    'property_id': row[1],
                    'predicted_value': row[2],
                    'actual_value': row[3],
                    'created_at': row[4]
                },
                'property': {
                    'med_income': row[5],
                    'house_age': row[6],
                    'ave_rooms': row[7],
                    'ave_bedrooms': row[8],
                    'population': row[9],
                    'ave_occupancy': row[10],
                    'latitude': row[11],
                    'longitude': row[12]
                }
            })
        
        cursor.close()
        return results