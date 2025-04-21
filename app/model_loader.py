# app/model_loader.py
import joblib  # o import pickle si usas .pkl
import os
from flask import current_app, g
import logging # Usar el logger de Flask

# Configurar un logger específico para el loader si quieres más detalle
log = logging.getLogger(__name__)

# Variable para almacenar el modelo cargado (para estrategia de carga única)
_prediction_model = None

def _load_model_from_path(model_path):
    """Función interna para cargar el modelo desde disco."""
    if not os.path.exists(model_path):
        log.error(f"Archivo de modelo no encontrado en: {model_path}")
        raise FileNotFoundError(f"Archivo de modelo no encontrado en: {model_path}")
    try:
        # Usa joblib.load si es .joblib, o pickle.load si es .pkl
        model = joblib.load(model_path)
        # con open(model_path, 'rb') as f:
        #     model = pickle.load(f) # para .pkl
        log.info(f"Modelo cargado exitosamente desde {model_path}")
        return model
    except Exception as e:
        log.exception(f"Error crítico al cargar el modelo desde {model_path}: {e}")
        raise  # Relanzar la excepción

def load_model_on_startup(app):
    """
    Carga el modelo una vez al iniciar la aplicación.
    Llamar desde create_app.
    """
    global _prediction_model
    if _prediction_model is None:
        model_path = app.config.get('MODEL_PATH')
        if not model_path:
             log.error("MODEL_PATH no está configurado en la aplicación Flask.")
             raise ValueError("La ruta del modelo (MODEL_PATH) no está configurada.")
        try:
             # Resuelve la ruta relativa a la instancia de la app si es necesario
             # if not os.path.isabs(model_path):
             #      model_path = os.path.join(app.instance_path, model_path) # O app.root_path
             log.info(f"Intentando cargar modelo desde: {model_path}")
             _prediction_model = _load_model_from_path(model_path)
             log.info("Modelo de predicción cargado globalmente.")
        except Exception as e:
             log.error(f"FALLO CRÍTICO: No se pudo cargar el modelo en el inicio. La aplicación puede no funcionar. Error: {e}")
             # Decide si la app debe fallar si el modelo no carga. Lanzar excepción es lo más seguro.
             raise RuntimeError(f"No se pudo cargar el modelo de predicción al inicio: {e}")

def get_prediction_model():
    """
    Obtiene la instancia del modelo (previamente cargado al inicio).
    """
    if _prediction_model is None:
        # Esto indica un problema en el flujo: load_model_on_startup no se llamó o falló.
        log.error("Intento de acceder al modelo antes de ser cargado o después de un fallo de carga.")
        raise RuntimeError("El modelo de predicción no está disponible. Contacte al administrador.")
    return _prediction_model

# --- (Nota sobre alternativa con 'g') ---
# Si prefieres cargar bajo demanda por request (menos eficiente si el modelo es grande):
# Define get_prediction_model usando 'g' como en la respuesta anterior
# y NO llames a load_model_on_startup en create_app.
# La carga única al inicio es generalmente preferible para modelos ML en producción.