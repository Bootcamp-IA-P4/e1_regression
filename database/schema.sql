-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS housing_predictions;
USE housing_predictions;

-- Tabla para propiedades inmobiliarias (alineada con las variables del modelo)
CREATE TABLE IF NOT EXISTS properties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Variables numéricas
    CalidadGeneral INT NOT NULL COMMENT 'Evaluación general de la condición de la vivienda (1-10)',
    MetrosHabitables FLOAT NOT NULL COMMENT 'Área habitable en metros cuadrados',
    CochesGaraje INT NOT NULL COMMENT 'Número de coches que caben en el garaje',
    ÁreaGaraje FLOAT NOT NULL COMMENT 'Superficie total del garaje en metros cuadrados',
    MetrosTotalesSótano FLOAT NOT NULL COMMENT 'Área total del sótano en metros cuadrados',
    Metros1raPlanta FLOAT NOT NULL COMMENT 'Superficie de la primera planta en metros cuadrados',
    BañosCompletos INT NOT NULL COMMENT 'Número de baños completos',
    TotalHabitacionesSobreSuelo INT NOT NULL COMMENT 'Número total de habitaciones sobre el nivel del suelo',
    AñoConstrucción INT NOT NULL COMMENT 'Año en que se construyó la vivienda',
    AñoRenovación INT NOT NULL COMMENT 'Año de la última renovación significativa',
    ÁreaRevestimientoMampostería FLOAT NOT NULL COMMENT 'Superficie de revestimiento de mampostería',
    Chimeneas INT NOT NULL COMMENT 'Número de chimeneas en la propiedad',
    MetrosAcabadosSótano1 FLOAT NOT NULL COMMENT 'Área acabada del primer sótano en metros cuadrados',
    FrenteLote FLOAT NOT NULL COMMENT 'Ancho del frente del lote',
    
    -- Variables categóricas
    CalidadExterior VARCHAR(10) NOT NULL COMMENT 'Calidad del material exterior (Fa, Gd, TA, Ex)',
    CalidadCocina VARCHAR(10) NOT NULL COMMENT 'Calidad de la cocina (Fa, Gd, TA, Ex)',
    CalidadSótano VARCHAR(10) NOT NULL COMMENT 'Calidad del sótano (Fa, Gd, NoSótano, TA, Ex)',
    AcabadoGaraje VARCHAR(10) NOT NULL COMMENT 'Acabado del garaje (NoGaraje, RFn, Unf, Fin)',
    AireAcondicionadoCentral VARCHAR(1) NOT NULL COMMENT 'Presencia de aire acondicionado central (Y, N)',
    CalidadChimenea VARCHAR(10) NOT NULL COMMENT 'Calidad de la chimenea (Fa, Gd, NoTiene, Po, TA, Ex)',
    Cimentación VARCHAR(10) NOT NULL COMMENT 'Tipo de cimentación (CBlock, PConc, Slab, Stone, Wood, BrkTil)',
    TipoGaraje VARCHAR(10) NOT NULL COMMENT 'Tipo de garaje (Attchd, Basment, BuiltIn, CarPort, Detchd, NoGaraje, 2Types)',
    TipoRevestimientoMampostería VARCHAR(10) NOT NULL COMMENT 'Tipo de revestimiento (BrkFace, Ninguno, Stone, BrkCmn)',
    CalidadCalefacción VARCHAR(10) NOT NULL COMMENT 'Calidad del sistema de calefacción (Fa, Gd, Po, TA, Ex)',
    Vecindario VARCHAR(20) NOT NULL COMMENT 'Nombre del vecindario',
    
    -- Otros campos de control
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla para registros de predicciones (mantiene la estructura relacional)
CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT NOT NULL,
    predicted_value FLOAT NOT NULL COMMENT 'Valor predicho por el modelo',
    actual_value FLOAT NULL COMMENT 'Valor real (para comparación, opcional)',
    prediction_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Índices para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_predictions_property ON predictions(property_id);
CREATE INDEX IF NOT EXISTS idx_properties_vecindario ON properties(Vecindario);
CREATE INDEX IF NOT EXISTS idx_properties_calidad ON properties(CalidadGeneral);
CREATE INDEX IF NOT EXISTS idx_properties_año ON properties(AñoConstrucción);