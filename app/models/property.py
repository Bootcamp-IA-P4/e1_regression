# app/models/property.py
from app.utils.db_utils import execute_query, insert_and_get_id
from flask import current_app
import logging

log = logging.getLogger(__name__)

class Property:
    """Modelo ORM-like para la tabla 'properties' (NUEVA ESTRUCTURA)."""

    def __init__(self, id=None,
                 calidad_general=None, metros_habitables=None, coches_garaje=None,
                 area_garaje=None, metros_totales_sotano=None, metros_1ra_planta=None,
                 banos_completos=None, total_habitaciones_sobre_suelo=None,
                 ano_construccion=None, ano_renovacion=None, area_revestimiento_mamposteria=None,
                 chimeneas=None, metros_acabados_sotano_1=None, frente_lote=None,
                 calidad_exterior=None, calidad_cocina=None, calidad_sotano=None,
                 acabado_garaje=None, aire_acondicionado_central=None, calidad_chimenea=None,
                 cimentacion=None, tipo_garaje=None, tipo_revestimiento_mamposteria=None,
                 calidad_calefaccion=None, vecindario=None, created_at=None):
        self.id = id
        self.calidad_general = calidad_general
        self.metros_habitables = metros_habitables
        self.coches_garaje = coches_garaje
        self.area_garaje = area_garaje
        self.metros_totales_sotano = metros_totales_sotano
        self.metros_1ra_planta = metros_1ra_planta
        self.banos_completos = banos_completos
        self.total_habitaciones_sobre_suelo = total_habitaciones_sobre_suelo
        self.ano_construccion = ano_construccion
        self.ano_renovacion = ano_renovacion
        self.area_revestimiento_mamposteria = area_revestimiento_mamposteria
        self.chimeneas = chimeneas
        self.metros_acabados_sotano_1 = metros_acabados_sotano_1
        self.frente_lote = frente_lote
        self.calidad_exterior = calidad_exterior
        self.calidad_cocina = calidad_cocina
        self.calidad_sotano = calidad_sotano
        self.acabado_garaje = acabado_garaje
        self.aire_acondicionado_central = aire_acondicionado_central
        self.calidad_chimenea = calidad_chimenea
        self.cimentacion = cimentacion
        self.tipo_garaje = tipo_garaje
        self.tipo_revestimiento_mamposteria = tipo_revestimiento_mamposteria
        self.calidad_calefaccion = calidad_calefaccion
        self.vecindario = vecindario
        self.created_at = created_at

    def to_dict(self, include_id=True):
        """Convierte el objeto a un diccionario."""
        data = {
            'calidad_general': self.calidad_general,
            'metros_habitables': self.metros_habitables,
            'coches_garaje': self.coches_garaje,
            'area_garaje': self.area_garaje,
            'metros_totales_sotano': self.metros_totales_sotano,
            'metros_1ra_planta': self.metros_1ra_planta,
            'banos_completos': self.banos_completos,
            'total_habitaciones_sobre_suelo': self.total_habitaciones_sobre_suelo,
            'ano_construccion': self.ano_construccion,
            'ano_renovacion': self.ano_renovacion,
            'area_revestimiento_mamposteria': self.area_revestimiento_mamposteria,
            'chimeneas': self.chimeneas,
            'metros_acabados_sotano_1': self.metros_acabados_sotano_1,
            'frente_lote': self.frente_lote,
            'calidad_exterior': self.calidad_exterior,
            'calidad_cocina': self.calidad_cocina,
            'calidad_sotano': self.calidad_sotano,
            'acabado_garaje': self.acabado_garaje,
            'aire_acondicionado_central': self.aire_acondicionado_central,
            'calidad_chimenea': self.calidad_chimenea,
            'cimentacion': self.cimentacion,
            'tipo_garaje': self.tipo_garaje,
            'tipo_revestimiento_mamposteria': self.tipo_revestimiento_mamposteria,
            'calidad_calefaccion': self.calidad_calefaccion,
            'vecindario': self.vecindario
            # created_at lo maneja la BD
        }
        if include_id and self.id:
            data['id'] = self.id
        if self.created_at:
             data['created_at'] = self.created_at
        return data

    @classmethod
    def _get_valid_attributes(cls):
        """Helper para obtener los nombres de los atributos válidos (excluyendo id y created_at)."""
        # Podríamos introspeccionar con inspect, pero hardcodear es más simple aquí
        return [
            'calidad_general', 'metros_habitables', 'coches_garaje', 'area_garaje',
            'metros_totales_sotano', 'metros_1ra_planta', 'banos_completos',
            'total_habitaciones_sobre_suelo', 'ano_construccion', 'ano_renovacion',
            'area_revestimiento_mamposteria', 'chimeneas', 'metros_acabados_sotano_1',
            'frente_lote', 'calidad_exterior', 'calidad_cocina', 'calidad_sotano',
            'acabado_garaje', 'aire_acondicionado_central', 'calidad_chimenea',
            'cimentacion', 'tipo_garaje', 'tipo_revestimiento_mamposteria',
            'calidad_calefaccion', 'vecindario'
        ]

    @classmethod
    def _from_db_row(cls, row):
        """Crea una instancia de Property desde un diccionario (fila de BD)."""
        if not row:
            return None
        # Filtra el diccionario 'row' para usar solo las claves que coinciden con los attrs esperados
        valid_attrs = cls._get_valid_attributes() + ['id', 'created_at']
        filtered_row = {k: v for k, v in row.items() if k in valid_attrs}
        return cls(**filtered_row) # Desempaqueta el diccionario filtrado

    def save(self):
        """Guarda (inserta o actualiza) la propiedad en la base de datos, aplicando defaults a Nones."""
        # 1. Obtenemos todos los atributos definidos del objeto
        data_to_save = {attr: getattr(self, attr, None) for attr in self._get_valid_attributes()}
        log.debug(f"Datos iniciales para guardar (desde objeto): {data_to_save}")

        # 2. Aplicar Defaults específicos para valores None antes de filtrar
        #    Ajusta este diccionario según las columnas que DEBEN tener un valor
        #    y cuyo default lógico es 0 (u otro valor) si falta el dato.
        #    Revisa tu schema.sql para ver qué es NOT NULL y no tiene DEFAULT SQL.
        defaults_if_none = {
            'area_revestimiento_mamposteria': 0.0,
            'metros_totales_sotano': 0.0,
            'area_garaje': 0.0,
            'coches_garaje': 0, # Entero
            'frente_lote': 0.0,  # O usa aquí el mismo valor de imputación que usaste en el entrenamiento si fue diferente de 0
            'metros_acabados_sotano_1': 0.0,
            'banos_completos': 0, # Entero
            'chimeneas': 0, # Entero
            # Considera otros campos numéricos que deberían ser 0 si no se especifican
            'metros_habitables': 0.0, # ¿Debería ser 0 si no se da? Probablemente no, es esencial
            'metros_1ra_planta': 0.0,  # Ídem
            # 'ano_construccion', 'ano_renovacion' probablemente no deberían tener default 0 aquí
        }
        for key, default_value in defaults_if_none.items():
            # Solo aplica si la clave existe en nuestro objeto Y su valor es None
            if key in data_to_save and data_to_save[key] is None:
                log.debug(f"Aplicando default '{default_value}' a '{key}' porque era None.")
                data_to_save[key] = default_value # Actualiza el diccionario data_to_save

        # 3. (Opcional pero recomendado) Manejar strings vacíos si no se hizo en routes.py
        #    Ejemplo: convertir "" para campos categóricos que significan 'NoTiene' o deben ser NULL
        string_to_value_mapping = {
             # 'calidad_sotano': {'': 'NoSótano'}, # O {'': None} si permite NULL
             # 'acabado_garaje': {'': 'NoGaraje'},
             # 'tipo_garaje':    { '': 'NoGaraje'},
             # Añade otros mapeos necesarios
        }
        for key, mapping in string_to_value_mapping.items():
            if key in data_to_save and data_to_save[key] in mapping:
                 original_value = data_to_save[key]
                 new_value = mapping[original_value]
                 log.debug(f"Convirtiendo string '{original_value}' en '{key}' a '{new_value}'.")
                 data_to_save[key] = new_value


        # 4. Filtrar atributos que TODAVÍA son None (después de aplicar defaults y tratar strings vacíos)
        #    Esto es para columnas que SÍ permiten NULL en la BD o cuya ausencia
        #    significa que no deben incluirse explícitamente en el INSERT/UPDATE.
        data_to_save_filtered = {k: v for k, v in data_to_save.items() if v is not None}
        log.debug(f"Datos después de aplicar defaults/mappings y filtrar Nones restantes: {data_to_save_filtered}")


        # 5. Validar si quedan datos para guardar
        if not data_to_save_filtered:
             log.error("No hay datos válidos para guardar en Property después de aplicar defaults y filtros.")
             # Podría devolver self o None, pero lanzar error es más explícito si falló el proceso
             raise ValueError("No se proporcionaron datos válidos para guardar la propiedad.")

        # 6. Ejecutar UPDATE o INSERT
        try:
            if self.id:
                # --- UPDATE ---
                # Filtrar claves que no existen en la BD (poco probable aquí, pero seguro)
                # update_data = {k: v for k, v in data_to_save_filtered.items() if k in self._get_valid_attributes()} # Redundante si ya filtramos antes
                if not data_to_save_filtered:
                    log.warning(f"Intento de actualizar Property ID {self.id} sin datos válidos (post-filtrado).")
                    return self # No hay nada que actualizar

                set_clause = ', '.join([f"`{k}`=%s" for k in data_to_save_filtered.keys()])
                query = f"UPDATE `properties` SET {set_clause} WHERE `id`=%s"
                params = tuple(data_to_save_filtered.values()) + (self.id,)
                affected_rows = execute_query(query, params, fetch_one=False, fetch_all=False) # Asegura que es escritura
                log.info(f"Property ID {self.id} actualizada. Filas afectadas: {affected_rows}")
                # Actualizar el objeto local con los datos guardados
                for k, v in data_to_save_filtered.items():
                    setattr(self, k, v)

            else:
                # --- INSERT ---
                last_id = insert_and_get_id('properties', data_to_save_filtered)
                if last_id:
                    self.id = last_id
                    # Actualizar el objeto local con los datos guardados
                    for k, v in data_to_save_filtered.items():
                        setattr(self, k, v)
                    log.info(f"Nueva Property creada con ID: {self.id}")
                else:
                    # insert_and_get_id debería lanzar excepción en error MySQL
                    log.error("insert_and_get_id devolvió None/0 sin lanzar excepción, indicando posible problema.")
                    # Lanzar un error aquí es más seguro que devolver None
                    raise RuntimeError("Falló la inserción de Property, no se obtuvo ID.")
            return self # Devuelve la instancia actualizada o recién creada

        except Exception as e:
            # El rollback ya debería ocurrir en execute_query o insert_and_get_id
            log.exception(f"Error de base de datos al guardar Property (ID: {self.id}): {e}")
            # Relanzar para que la capa superior (ruta) lo maneje (muestre flash, etc.)
            raise # ¡Importante relanzar!

    @classmethod
    def find_by_id(cls, property_id):
        """Busca una propiedad por su ID."""
        query = "SELECT * FROM `properties` WHERE `id` = %s"
        try:
            result_row = execute_query(query, (property_id,), fetch_one=True)
            return cls._from_db_row(result_row)
        except Exception as e:
            log.exception(f"Error al buscar Property por ID {property_id}: {e}")
            return None

    @classmethod
    def find_all(cls, limit=100, offset=0):
        """Busca todas las propiedades con paginación opcional."""
        # Podrías querer ordenar por algo diferente a created_at si esa columna no existe
        query = "SELECT * FROM `properties` ORDER BY `id` DESC LIMIT %s OFFSET %s"
        properties = []
        try:
            results = execute_query(query, (limit, offset), fetch_all=True)
            if results:
                properties = [cls._from_db_row(row) for row in results if row]
            return properties
        except Exception as e:
            log.exception(f"Error al buscar todas las Properties: {e}")
            return []

    @classmethod
    def create(cls, **kwargs):
       """Método de conveniencia para crear y guardar una nueva propiedad."""
       valid_args = {k: v for k, v in kwargs.items() if k in cls._get_valid_attributes()}
       instance = cls(**valid_args)
       return instance.save()