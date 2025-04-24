import pickle 
import numpy as np
import os
import pandas as pd
from flask import current_app, g
import logging

log = logging.getLogger(__name__)
# _prediction_model ahora contendrá el diccionario completo cargado
_prediction_model = None
_model = None

def _load_model_from_path(model_path):
    """Carga el contenido del PKL y valida si es un diccionario con 'modelo'."""
    if not os.path.exists(model_path):
        log.error(f"Archivo de modelo no encontrado en: {model_path}")
        raise FileNotFoundError(f"Archivo de modelo no encontrado en: {model_path}")
    try:
        with open(model_path, 'rb') as f:
             loaded_object = pickle.load(f)

        # Validar el objeto cargado, pero devolver el objeto COMPLETO (el diccionario)
        if isinstance(loaded_object, dict):
            log.debug(f"Archivo PKL contenía un diccionario. Claves: {loaded_object.keys()}")
            if 'modelo' in loaded_object and hasattr(loaded_object['modelo'], 'predict'):
                 log.info("Diccionario validado: Contiene clave 'modelo' con un objeto predictivo.")
                 # NO extraemos el modelo aquí, devolvemos el dict original
            else:
                log.error("Diccionario en PKL no contiene clave 'modelo' o el valor no es un modelo predictivo.")
                raise KeyError("Diccionario en PKL no tiene el formato esperado (falta 'modelo' predictivo).")
        # Si se cargó directamente el modelo (caso menos probable ahora)
        elif hasattr(loaded_object, 'predict'):
             log.warning("Archivo PKL contenía directamente un modelo, no un diccionario. Adaptando...")
             # Crear un diccionario compatible para que el resto del código funcione
             # ASUNCIÓN: Necesitarías cargar el scaler y listas de otro lado o hardcodearlos
             # Esto es MENOS IDEAL. Lo mejor es que el PKL siempre tenga la misma estructura (dict).
             # loaded_object = {'modelo': loaded_object, 'scaler': None, ...} # Ejemplo
             raise TypeError("El PKL contenía solo el modelo, se esperaba un diccionario con componentes.")
        else:
            log.error(f"El objeto cargado desde {model_path} no tiene formato esperado. Tipo: {type(loaded_object)}")
            raise TypeError(f"El contenido de {model_path} no es un diccionario reconocible con el modelo.")

        log.info(f"Contenido PKL cargado y validado desde {model_path}")
        # Devolver el objeto cargado (que validamos es un diccionario con lo necesario)
        return loaded_object # <--- ¡DEVUELVE EL DICCIONARIO COMPLETO!

    except FileNotFoundError:
         raise
    except (pickle.UnpicklingError, KeyError, TypeError) as e:
         log.exception(f"Error al procesar/validar el contenido de {model_path}: {e}")
         raise RuntimeError(f"Error al procesar el archivo del modelo: {e}") from e
    except Exception as e:
         log.exception(f"Error inesperado al cargar el modelo desde {model_path}: {e}")
         raise

def load_model_on_startup(app):
    """Carga el diccionario completo del modelo al iniciar la aplicación."""
    global _prediction_model

    if _prediction_model is None:
        model_path = app.config.get('MODEL_PATH')
        if not model_path:
             log.error("MODEL_PATH no está configurado.")
             raise ValueError("La ruta del modelo (MODEL_PATH) no está configurada.")
        try:
             log.info(f"Intentando cargar diccionario de modelo desde: {model_path}")
             # _load_model_from_path ahora devuelve el diccionario
             _prediction_model = _load_model_from_path(model_path)
             log.info("Diccionario de componentes del modelo cargado globalmente.")
        except Exception as e:
             # El error ya fue loggeado por _load_model_from_path o aquí
             log.critical(f"La carga del diccionario del modelo falló. Error: {e}")
             
             _prediction_model = None
             raise RuntimeError(f"No se pudo cargar el diccionario del modelo: {e}") 

def get_prediction_model(): # Nombre quizá confuso, pero lo mantenemos por ahora
    """
    Obtiene el DICCIONARIO completo de componentes del modelo cargado.
    """
    if _prediction_model is None:
        log.error("Intento de acceder a los componentes del modelo antes de ser cargados o después de un fallo de carga.")
        # Este error es ahora MÁS PROBABLE si la carga falló en load_model_on_startup
        raise RuntimeError("Los componentes del modelo no están disponibles. Faltan o hubo error al cargar.")
    return _prediction_model 

def prepare_data_for_prediction(property_data, model_components):
    """Prepara los datos para la predicción aplicando la misma transformación que en el entrenamiento."""
    log.info(f"Variables numéricas esperadas: {model_components.get('variables_numericas', [])}")
    log.info(f"Variables categóricas esperadas: {model_components.get('variables_categoricas_originales', [])}")
    # Extraer los componentes necesarios
    scaler = model_components.get('scaler')
    variables_numericas = model_components.get('variables_numericas', [])
    variables_categoricas = model_components.get('variables_categoricas_originales', [])
    
    # Crear un DataFrame con una sola fila
    import pandas as pd
    import numpy as np
    
    # Crear diccionario para el DataFrame
    data_dict = {}
    
    # Agregar variables numéricas
    for var in variables_numericas:
        data_dict[var] = [property_data.get(var, 0)]
    
    # Agregar variables categóricas
    for var in variables_categoricas:
        data_dict[var] = [property_data.get(var, '')]
    
    # Crear DataFrame
    df = pd.DataFrame(data_dict)
    
    # Aplicar one-hot encoding a las variables categóricas
    if variables_categoricas:
        df_encoded = pd.get_dummies(df, columns=variables_categoricas, drop_first=False)
        
        # Asegurarse de que todas las columnas del entrenamiento estén presentes
        for col in model_components.get('variables_categoricas_encoded', []):
            if col not in df_encoded.columns:
                df_encoded[col] = 0
        
        # Reordenar las columnas para que coincidan con el entrenamiento
        all_features = variables_numericas + model_components.get('variables_categoricas_encoded', [])
        df_final = df_encoded[all_features]
    else:
        df_final = df
        log.info(f"DataFrame final antes de escalar: {df_final.head()}")
    
    # Escalar variables numéricas si hay un scaler
    if scaler is not None:
        df_final[variables_numericas] = scaler.transform(df_final[variables_numericas])
        log.info(f"DataFrame final después de escalar: {df_final.head()}")
    
    return df_final

def predict_house_price(property_data):
    """Realiza una predicción con el modelo cargado."""
    try:
        # Verificar datos de entrada
        log.info(f"DATOS DE ENTRADA: {property_data}")
        
        # NUEVO: Convertir nombres de snake_case a PascalCase con acentos
        name_mapping = {
            'calidad_general': 'CalidadGeneral',
            'metros_habitables': 'MetrosHabitables',
            'coches_garaje': 'CochesGaraje',
            'area_garaje': 'ÁreaGaraje',
            'metros_totales_sotano': 'MetrosTotalesSótano',
            'metros_1ra_planta': 'Metros1raPlanta',
            'banos_completos': 'BañosCompletos',
            'total_habitaciones_sobre_suelo': 'TotalHabitacionesSobreSuelo',
            'ano_construccion': 'AñoConstrucción',
            'ano_renovacion': 'AñoRenovación',
            'area_revestimiento_mamposteria': 'ÁreaRevestimientoMampostería',
            'chimeneas': 'Chimeneas',
            'metros_acabados_sotano_1': 'MetrosAcabadosSótano1',
            'frente_lote': 'FrenteLote',
            'calidad_exterior': 'CalidadExterior',
            'calidad_cocina': 'CalidadCocina',
            'calidad_sotano': 'CalidadSótano',
            'acabado_garaje': 'AcabadoGaraje',
            'aire_acondicionado_central': 'AireAcondicionadoCentral',
            'calidad_chimenea': 'CalidadChimenea',
            'cimentacion': 'Cimentación',
            'tipo_garaje': 'TipoGaraje',
            'tipo_revestimiento_mamposteria': 'TipoRevestimientoMampostería',
            'calidad_calefaccion': 'CalidadCalefacción',
            'vecindario': 'Vecindario'
        }
        
        # Crear un nuevo diccionario con los nombres convertidos
        converted_data = {}
        for key, value in property_data.items():
            if key in name_mapping:
                converted_data[name_mapping[key]] = value
            else:
                converted_data[key] = value
        
        log.info(f"DATOS CONVERTIDOS: {converted_data}")
        
        # Usar los datos convertidos para el resto de la función
        if _prediction_model is None:
            raise ValueError("El modelo no ha sido cargado. Ejecute load_model_on_startup primero.")
        
        # Verificación de nombres de variables
        variables_esperadas_num = set(_prediction_model.get('variables_numericas', []))
        variables_esperadas_cat = set(_prediction_model.get('variables_categoricas_originales', []))
        variables_recibidas = set(converted_data.keys())  # ¡Ahora usamos converted_data!
        
        # Verificar si faltan variables importantes
        missing_vars = (variables_esperadas_num.union(variables_esperadas_cat)) - variables_recibidas
        if missing_vars:
            log.warning(f"Faltan variables necesarias: {missing_vars}")
        
        # Acceder al modelo dentro del diccionario
        model = _prediction_model['modelo']
        
        # Verificar tipo de modelo
        log.info(f"TIPO DE MODELO: {type(model)}")
        
        # Preparar datos con más logs
        X_processed = prepare_data_for_prediction(converted_data, _prediction_model)  # ¡Usar converted_data!
        
        # Realizar predicción
        prediction = model.predict(X_processed)
        log.info(f"PREDICCIÓN RAW: {prediction}")
        
        # Transformar si es necesario
        if _prediction_model.get('transformacion_log', False):
            log_pred = prediction[0]
            prediction = np.exp(prediction)
            log.info(f"Transformando predicción: log {log_pred} -> exp {prediction[0]}")
        
        return float(prediction[0])
        
    except Exception as e:
        log.error(f"Error al realizar predicción: {e}", exc_info=True)
        raise