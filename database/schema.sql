-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS housing_predictions;
USE housing_predictions;

-- Tabla para propiedades inmobiliarias (actualizada)
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
    calidad_general INT COMMENT 'Evaluación general de la condición de la vivienda',
    metros_habitables FLOAT COMMENT 'Área habitable en metros cuadrados',
    coches_garaje INT COMMENT 'Número de coches en el garaje',
    area_garaje FLOAT COMMENT 'Superficie total del garaje en metros cuadrados',
    metros_totales_sotano FLOAT COMMENT 'Área total del sótano en metros cuadrados',
    metros_1ra_planta FLOAT COMMENT 'Superficie de la primera planta en metros cuadrados',
    baños_completos INT COMMENT 'Número de baños completos',
    total_habitaciones_sobre_suelo INT COMMENT 'Número total de habitaciones sobre el nivel del suelo',
    año_construcción INT COMMENT 'Año de construcción de la vivienda',
    año_renovación INT COMMENT 'Año de la última renovación significativa',
    area_revestimiento_mampostería FLOAT COMMENT 'Superficie de revestimiento de mampostería',
    chimeneas INT COMMENT 'Número de chimeneas',
    metros_acabados_sotano1 FLOAT COMMENT 'Área acabada del primer sótano en metros cuadrados',
    frente_lote FLOAT COMMENT 'Ancho del frente del lote',
    calidad_exterior ENUM('Fa', 'Gd', 'TA') COMMENT 'Calidad exterior',
    calidad_cocina ENUM('Fa', 'Gd', 'TA') COMMENT 'Calidad de la cocina',
    calidad_sotano ENUM('Fa', 'Gd', 'NoSótano', 'TA') COMMENT 'Calidad del sótano',
    acabado_garaje ENUM('NoGaraje', 'RFn', 'Unf') COMMENT 'Acabado del garaje',
    aire_acondicionado_central ENUM('Y') COMMENT 'Aire acondicionado central',
    calidad_chimenea ENUM('Fa', 'Gd', 'NoTiene', 'Po', 'TA') COMMENT 'Calidad de la chimenea',
    cimentación ENUM('CBlock', 'PConc', 'Slab', 'Stone', 'Wood') COMMENT 'Cimentación',
    tipo_garaje ENUM('Attchd', 'Basment', 'BuiltIn', 'CarPort', 'Detchd', 'NoGaraje') COMMENT 'Tipo de garaje',
    tipo_revestimiento_mampostería ENUM('BrkFace', 'Ninguno', 'Stone') COMMENT 'Tipo de revestimiento de mampostería',
    calidad_calefacción ENUM('Fa', 'Gd', 'Po', 'TA') COMMENT 'Calidad de la calefacción',
    vecindario VARCHAR(50) COMMENT 'Vecindario codificado',
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