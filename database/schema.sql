-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS housing_predictions;
USE housing_predictions;

-- Tabla para propiedades inmobiliarias
CREATE TABLE IF NOT EXISTS properties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    med_income FLOAT NOT NULL COMMENT 'Ingreso medio de la zona',
    house_age FLOAT NOT NULL COMMENT 'Edad media de las casas en la zona',
    ave_rooms FLOAT NOT NULL COMMENT 'Promedio de habitaciones por casa',
    ave_bedrooms FLOAT NOT NULL COMMENT 'Promedio de dormitorios por casa',
    population FLOAT NOT NULL COMMENT 'Población de la zona',
    ave_occupancy FLOAT NOT NULL COMMENT 'Promedio de ocupantes por casa',
    latitude FLOAT NOT NULL COMMENT 'Latitud',
    longitude FLOAT NOT NULL COMMENT 'Longitud',
    median_value FLOAT COMMENT 'Valor medio real (si se conoce)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla para registros de predicciones
CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT NOT NULL,
    predicted_value FLOAT NOT NULL COMMENT 'Valor predicho por el modelo',
    actual_value FLOAT COMMENT 'Valor real (para comparación)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Índices para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_predictions_property ON predictions(property_id);
CREATE INDEX IF NOT EXISTS idx_predictions_created ON predictions(created_at);