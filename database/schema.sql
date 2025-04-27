-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS housing_predictions;
USE housing_predictions;

-- Tabla para propiedades inmobiliarias (actualizada para Ames Housing)
CREATE TABLE IF NOT EXISTS properties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    calidad_general INT NOT NULL COMMENT 'Calidad general de la vivienda (1-10)',
    metros_habitables FLOAT NOT NULL COMMENT 'Área total habitable en metros cuadrados',
    coches_garaje INT NOT NULL DEFAULT 0 COMMENT 'Capacidad del garaje en coches',
    area_garaje FLOAT NOT NULL DEFAULT 0 COMMENT 'Superficie del garaje en metros cuadrados',
    metros_totales_sotano FLOAT NOT NULL DEFAULT 0 COMMENT 'Superficie total del sótano',
    metros_1ra_planta FLOAT NOT NULL DEFAULT 0 COMMENT 'Superficie de la primera planta',
    banos_completos INT NOT NULL DEFAULT 0 COMMENT 'Número de baños completos',
    total_habitaciones_sobre_suelo INT NOT NULL COMMENT 'Total de habitaciones sobre el nivel del suelo',
    ano_construccion INT NOT NULL COMMENT 'Año de construcción',
    ano_renovacion INT NOT NULL COMMENT 'Año de última renovación',
    area_revestimiento_mamposteria FLOAT NOT NULL DEFAULT 0 COMMENT 'Superficie de revestimiento de mampostería',
    chimeneas INT NOT NULL DEFAULT 0 COMMENT 'Número de chimeneas',
    metros_acabados_sotano_1 FLOAT NOT NULL DEFAULT 0 COMMENT 'Superficie acabada del sótano',
    frente_lote FLOAT NOT NULL DEFAULT 0 COMMENT 'Ancho del frente del lote en metros',
    calidad_exterior VARCHAR(10) NOT NULL COMMENT 'Calidad del material exterior (Ex, Gd, TA, Fa)',
    calidad_cocina VARCHAR(10) NOT NULL COMMENT 'Calidad de la cocina (Ex, Gd, TA, Fa)',
    calidad_sotano VARCHAR(10) NOT NULL COMMENT 'Calidad del sótano (Ex, Gd, TA, Fa, NoSótano)',
    acabado_garaje VARCHAR(10) NOT NULL COMMENT 'Tipo de acabado del garaje (Fin, RFn, Unf, NoGaraje)',
    aire_acondicionado_central CHAR(1) NOT NULL COMMENT 'Si tiene aire acondicionado central (Y/N)',
    calidad_chimenea VARCHAR(10) NOT NULL COMMENT 'Calidad de la chimenea (Ex, Gd, TA, Fa, Po, NoTiene)',
    cimentacion VARCHAR(10) NOT NULL COMMENT 'Tipo de cimentación (PConc, CBlock, BrkTil, Stone, Wood, Slab)',
    tipo_garaje VARCHAR(10) NOT NULL COMMENT 'Tipo de garaje (Attchd, Detchd, BuiltIn, CarPort, NoGaraje, Basment, 2Types)',
    tipo_revestimiento_mamposteria VARCHAR(10) NOT NULL COMMENT 'Tipo de revestimiento (BrkFace, Stone, BrkCmn, Ninguno)',
    calidad_calefaccion VARCHAR(10) NOT NULL COMMENT 'Calidad del sistema de calefacción (Ex, Gd, TA, Fa, Po)',
    vecindario VARCHAR(20) NOT NULL COMMENT 'Vecindario donde se encuentra la propiedad',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de creación del registro'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla para registros de predicciones
CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT NOT NULL,
    predicted_value FLOAT NOT NULL COMMENT 'Valor predicho por el modelo (en dólares)',
    actual_value FLOAT COMMENT 'Valor real si se conoce (para comparación)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla de usuarios (si es necesario)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Índices para mejorar el rendimiento
CREATE INDEX idx_predictions_property ON predictions(property_id);
CREATE INDEX idx_predictions_created ON predictions(created_at);
CREATE INDEX idx_properties_calidad ON properties(calidad_general);
CREATE INDEX idx_properties_vecindario ON properties(vecindario);