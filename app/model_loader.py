# app/model_loader.py
import joblib
import pickle # Asegúrate de tenerlo importado
import os
from flask import current_app, g
import logging

log = logging.getLogger(__name__)
# _prediction_model ahora contendrá el diccionario completo cargado
_prediction_model = None

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
             # Mantenemos _prediction_model como None si falla
             _prediction_model = None # Asegurar que quede None
             # No relanzamos aquí para que la app intente arrancar, pero las rutas fallarán
             # raise RuntimeError(f"No se pudo cargar el diccionario del modelo: {e}")

def get_prediction_model(): # Nombre quizá confuso, pero lo mantenemos por ahora
    """
    Obtiene el DICCIONARIO completo de componentes del modelo cargado.
    """
    if _prediction_model is None:
        log.error("Intento de acceder a los componentes del modelo antes de ser cargados o después de un fallo de carga.")
        # Este error es ahora MÁS PROBABLE si la carga falló en load_model_on_startup
        raise RuntimeError("Los componentes del modelo no están disponibles. Faltan o hubo error al cargar.")
    return _prediction_model # <--- DEVUELVE EL DICCIONARIO