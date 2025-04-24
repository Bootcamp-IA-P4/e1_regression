-- Insertar datos iniciales en la tabla properties
INSERT INTO properties (
    med_income, house_age, ave_rooms, ave_bedrooms, population, ave_occupancy, latitude, longitude, median_value,
    calidad_general, metros_habitables, coches_garaje, area_garaje, metros_totales_sotano, metros_1ra_planta,
    baños_completos, total_habitaciones_sobre_suelo, año_construcción, año_renovación, area_revestimiento_mampostería,
    chimeneas, metros_acabados_sotano1, frente_lote, calidad_exterior, calidad_cocina, calidad_sotano, acabado_garaje,
    aire_acondicionado_central, calidad_chimenea, cimentación, tipo_garaje, tipo_revestimiento_mampostería,
    calidad_calefacción, vecindario
) VALUES (
    3.5, 20, 6.5, 1.5, 1200, 3.2, 37.7749, -122.4194, 450000,
    7, 120, 2, 30, 60, 80,
    2, 8, 1995, 2010, 15,
    1, 30, 20, 'Gd', 'TA', 'TA', 'RFn',
    'Y', 'Gd', 'PConc', 'Attchd', 'BrkFace',
    'Gd', 'Somerst'
);