-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS housing_predictions;
USE housing_predictions;

-- Tabla para propiedades inmobiliarias
CREATE TABLE IF NOT EXISTS properties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    calidad_general INT,
    metros_habitables FLOAT,
    coches_garaje INT,
    area_garaje FLOAT,
    metros_totales_sotano FLOAT,
    metros_1ra_planta FLOAT,
    banos_completos INT,
    total_habitaciones_sobre_suelo INT,
    ano_construccion INT,
    ano_renovacion INT,
    area_revestimiento_mamposteria FLOAT,
    chimeneas INT,
    metros_acabados_sotano_1 FLOAT,
    frente_lote FLOAT,
    calidad_exterior VARCHAR(10),
    calidad_cocina VARCHAR(10),
    calidad_sotano VARCHAR(15),
    acabado_garaje VARCHAR(10),
    aire_acondicionado_central VARCHAR(2),
    calidad_chimenea VARCHAR(10),
    cimentacion VARCHAR(10),
    tipo_garaje VARCHAR(15),
    tipo_revestimiento_mamposteria VARCHAR(15),
    calidad_calefaccion VARCHAR(10),
    vecindario VARCHAR(20),
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