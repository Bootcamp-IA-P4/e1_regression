from app import mysql

class Property:
    """Modelo para representar propiedades inmobiliarias en la base de datos."""
    
    def __init__(self, id=None, med_income=None, house_age=None, ave_rooms=None, 
                 ave_bedrooms=None, population=None, ave_occupancy=None, 
                 latitude=None, longitude=None, median_value=None):
        self.id = id
        self.med_income = med_income
        self.house_age = house_age
        self.ave_rooms = ave_rooms
        self.ave_bedrooms = ave_bedrooms
        self.population = population
        self.ave_occupancy = ave_occupancy
        self.latitude = latitude
        self.longitude = longitude
        self.median_value = median_value
    
    def save(self):
        """Guarda la propiedad en la base de datos."""
        cursor = mysql.connection.cursor()
        
        if self.id:
            # Actualizar registro existente
            cursor.execute('''
                UPDATE properties 
                SET med_income=%s, house_age=%s, ave_rooms=%s, ave_bedrooms=%s,
                    population=%s, ave_occupancy=%s, latitude=%s, longitude=%s, median_value=%s
                WHERE id=%s
            ''', (
                self.med_income, self.house_age, self.ave_rooms, self.ave_bedrooms,
                self.population, self.ave_occupancy, self.latitude, self.longitude,
                self.median_value, self.id
            ))
        else:
            # Insertar nuevo registro
            cursor.execute('''
                INSERT INTO properties (
                    med_income, house_age, ave_rooms, ave_bedrooms, population, 
                    ave_occupancy, latitude, longitude, median_value
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                self.med_income, self.house_age, self.ave_rooms, self.ave_bedrooms,
                self.population, self.ave_occupancy, self.latitude, self.longitude,
                self.median_value
            ))
            self.id = cursor.lastrowid
        
        mysql.connection.commit()
        cursor.close()
        return self
    
    @staticmethod
    def get_by_id(property_id):
        """Obtiene una propiedad por su ID."""
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM properties WHERE id = %s', (property_id,))
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return Property(
                id=result[0], med_income=result[1], house_age=result[2],
                ave_rooms=result[3], ave_bedrooms=result[4], population=result[5],
                ave_occupancy=result[6], latitude=result[7], longitude=result[8],
                median_value=result[9]
            )
        return None

    @staticmethod
    def get_all(limit=100):
        """Obtiene todas las propiedades."""
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM properties LIMIT %s', (limit,))
        properties = []
        
        for row in cursor.fetchall():
            properties.append(Property(
                id=row[0], med_income=row[1], house_age=row[2],
                ave_rooms=row[3], ave_bedrooms=row[4], population=row[5],
                ave_occupancy=row[6], latitude=row[7], longitude=row[8],
                median_value=row[9]
            ))
        
        cursor.close()
        return properties