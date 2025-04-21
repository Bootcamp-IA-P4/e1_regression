# app/routes.py
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, current_app, jsonify
)
import pandas as pd
from app.model_loader import get_prediction_model # Modelo ML
from app.models.property import Property           # Modelo de datos Property
from app.models.prediction import Prediction         # Modelo de datos Prediction
import logging

log = logging.getLogger(__name__)

main_bp = Blueprint('main', __name__, template_folder='templates', static_folder='static')
# Si templates/static están en app/, Flask los encuentra aunque no los especifiques aquí explícitamente si están en app/

@main_bp.route('/')
def index():
    """Página principal: Muestra formulario y lista de predicciones recientes."""
    recent_predictions_data = []
    try:
        # Obtener datos combinados de predicción y propiedad
        recent_predictions_data = Prediction.get_recent_with_property(limit=10)
    except Exception as e:
        log.exception("Error al obtener predicciones recientes para la página principal.")
        flash('No se pudieron cargar las predicciones recientes.', 'error')
        # Renderizar igualmente la página, pero estará vacía la tabla

    # Pasa los datos directamente a la plantilla
    return render_template('index.html', recent_predictions=recent_predictions_data)


@main_bp.route('/predict', methods=['GET', 'POST'])
def predict_page():
    """Página para realizar una nueva predicción (muestra formulario y resultado)."""

    if request.method == 'POST':
        form_data = request.form.to_dict() # Obtener datos del formulario como dict
        property_input_data = {}
        model_features = {}

        try:
            # 1. Validar y convertir datos del formulario
            # Nombres clave deben coincidir con los <input name="...">
            feature_map = {
                'MedInc': 'med_income', 'HouseAge': 'house_age', 'AveRooms': 'ave_rooms',
                'AveBedrms': 'ave_bedrooms', 'Population': 'population', 'AveOccup': 'ave_occupancy',
                'Latitude': 'latitude', 'Longitude': 'longitude'
            }
            for form_key, model_key in feature_map.items():
                value_str = form_data.get(form_key)
                if value_str is None or value_str.strip() == '':
                     raise ValueError(f"El campo '{form_key}' es requerido.")
                try:
                    value_float = float(value_str)
                    property_input_data[model_key] = value_float # Para guardar en Property
                    model_features[form_key] = value_float      # Para alimentar al modelo ML
                except ValueError:
                     raise ValueError(f"El valor '{value_str}' para '{form_key}' no es un número válido.")

            # 2. Preparar datos para el modelo ML
            df_predict = pd.DataFrame([model_features]) # El modelo espera un DataFrame

            # 3. Obtener el modelo y predecir
            log.debug(f"Realizando predicción con datos: {model_features}")
            model = get_prediction_model() # Obtiene el modelo cargado al inicio
            predicted_value = model.predict(df_predict)[0]
            predicted_value = float(predicted_value) # Asegurar tipo Python float
            log.info(f"Predicción obtenida: {predicted_value}")

            # 4. Guardar la propiedad y la predicción
            # Usar el método de clase que crea ambos
            saved_property, saved_prediction = Prediction.create_from_data(
                property_data=property_input_data,
                prediction_data={'predicted_value': predicted_value}
                # actual_value se puede añadir aquí si se tuviera
            )

            if not saved_property or not saved_prediction:
                 # El error ya fue loggeado por create_from_data
                 flash('Error al guardar los resultados de la predicción en la base de datos.', 'error')
                 # Re-renderizar el formulario con los datos y el error
                 return render_template('predict.html',
                                        form_data=form_data, # Devolver datos originales del form
                                        error_message='No se pudo guardar el resultado.'), 500
            else:
                 flash(f'Predicción realizada y guardada (Propiedad ID: {saved_property.id}, Predicción ID: {saved_prediction.id}).', 'success')
                 # Renderizar la misma página pero mostrando el resultado
                 return render_template('predict.html',
                                        prediction_result=predicted_value,
                                        input_data=property_input_data, # Datos usados formateados
                                        form_data=form_data, # Para mostrar lo ingresado
                                        prediction_saved=True)

        except ValueError as e:
            log.warning(f"Error de validación en formulario de predicción: {e}")
            flash(f'Error en los datos ingresados: {e}', 'warning')
            # Re-renderizar el formulario con los datos originales y el mensaje flash
            return render_template('predict.html', form_data=form_data), 400 # Bad request
        except FileNotFoundError as e:
            log.error(f"Error crítico: no se encontró el archivo del modelo - {e}")
            flash('Error interno del servidor: el modelo de predicción no está disponible.', 'danger')
            return render_template('predict.html', form_data=form_data), 500
        except RuntimeError as e: # Errores del loader o de BD relanzados
             log.error(f"Error de ejecución durante la predicción: {e}")
             flash(f'Error interno del servidor: {e}', 'danger')
             return render_template('predict.html', form_data=form_data), 500
        except Exception as e:
            log.exception("Error inesperado en la ruta /predict [POST]") # Log completo
            flash('Ocurrió un error inesperado procesando la solicitud.', 'danger')
            return render_template('predict.html', form_data=form_data), 500

    # Método GET: Mostrar formulario vacío la primera vez
    return render_template('predict.html', form_data={})

# --- Endpoint API (Opcional) ---
@main_bp.route('/api/v1/predictions', methods=['POST'])
def api_create_prediction():
    if not request.is_json:
        log.warning("API request recibido sin content-type application/json")
        return jsonify({"error": "La solicitud debe ser JSON (Content-Type: application/json)"}), 415

    data = request.get_json()
    if not data:
        log.warning("API request recibido con JSON vacío o inválido.")
        return jsonify({"error": "Cuerpo JSON inválido o vacío."}), 400

    log.debug(f"API Request recibido: {data}")

    # 1. Validar y mapear datos JSON
    required_features = ['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population', 'AveOccup', 'Latitude', 'Longitude']
    property_input_data = {}
    model_features = {}
    feature_map = {k: k.lower().replace(' ', '_') for k in required_features} # Mapeo simple para DB
    feature_map.update({ # Actualizar mapeo si nombres difieren mucho
        'MedInc': 'med_income', 'HouseAge': 'house_age', 'AveRooms': 'ave_rooms',
        'AveBedrms': 'ave_bedrooms', 'Population': 'population', 'AveOccup': 'ave_occupancy',
        'Latitude': 'latitude', 'Longitude': 'longitude'
        })


    missing_fields = [f for f in required_features if f not in data]
    if missing_fields:
         log.warning(f"API request con campos faltantes: {missing_fields}")
         return jsonify({"error": "Campos requeridos faltantes.", "missing": missing_fields}), 400

    try:
        for feature_key in required_features:
             db_key = feature_map[feature_key]
             value = float(data[feature_key]) # Intentar convertir a float
             property_input_data[db_key] = value
             model_features[feature_key] = value

        actual_value = data.get('ActualValue') # Opcional
        if actual_value is not None:
             actual_value = float(actual_value)

    except (ValueError, TypeError) as e:
        log.warning(f"API request con tipos de datos inválidos: {e}")
        return jsonify({"error": f"Tipo de dato inválido en la entrada: {e}"}), 400

    try:
        # 2. Predecir
        df_predict = pd.DataFrame([model_features])
        model = get_prediction_model()
        predicted_value = float(model.predict(df_predict)[0])
        log.info(f"API Predicción: {predicted_value} para datos {model_features}")

        # 3. Guardar
        saved_property, saved_prediction = Prediction.create_from_data(
             property_data=property_input_data,
             prediction_data={
                 'predicted_value': predicted_value,
                 'actual_value': actual_value # Pasará None si no se proporcionó
            }
        )

        if not saved_property or not saved_prediction:
            log.error("API: Falló el guardado de propiedad/predicción.")
            return jsonify({"error": "Error interno al guardar los datos."}), 500

        # 4. Respuesta Exitosa
        response_data = {
            "message": "Predicción creada exitosamente.",
            "property": saved_property.to_dict(),
            "prediction": saved_prediction.to_dict()
        }
        log.info(f"API Predicción creada: Property ID {saved_property.id}, Prediction ID {saved_prediction.id}")
        # Devolver URL al recurso creado es buena práctica REST
        # prediction_url = url_for('main.api_get_prediction', prediction_id=saved_prediction.id, _external=True)
        return jsonify(response_data), 201 # Código 201 Created
        # return jsonify(response_data), 201, {'Location': prediction_url} # Con cabecera Location

    except FileNotFoundError as e:
        log.error(f"API Error crítico: no se encontró el archivo del modelo - {e}")
        return jsonify({"error": "Error interno del servidor: modelo no disponible."}), 500
    except RuntimeError as e:
        log.error(f"API Error de ejecución: {e}")
        return jsonify({"error": f"Error interno del servidor: {e}"}), 500
    except Exception as e:
        log.exception("API Error inesperado [POST /api/v1/predictions]")
        return jsonify({"error": "Ocurrió un error inesperado."}), 500


# Podrías añadir un endpoint GET para recuperar una predicción específica por ID
# @main_bp.route('/api/v1/predictions/<int:prediction_id>', methods=['GET'])
# def api_get_prediction(prediction_id):
#    ... busca la predicción ...
#    if not prediction:
#        return jsonify({"error": "Predicción no encontrada"}), 404
#    return jsonify(prediction.to_dict()), 200