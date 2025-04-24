# app/routes.py (Versión Completa, Corregida para Ames con Reordenado)

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from .models.prediction import Prediction
from .models.property import Property
from .model_loader import predict_house_price
import logging

log = logging.getLogger(__name__)
main_bp = Blueprint('main', __name__, 
                   static_folder='static',
                   static_url_path='/main/static')

@main_bp.route('/')
def index():
    """Página principal con listado de predicciones recientes."""
    try:
        recent_predictions = Prediction.get_recent_with_property()
        return render_template('index.html', recent_predictions=recent_predictions)
    except Exception as e:
        log.error(f"Error al obtener predicciones: {e}")
        flash(f"Error al cargar predicciones: {str(e)}", "danger")
        return render_template('index.html', recent_predictions=[])

@main_bp.route('/predict', methods=['GET', 'POST'])
def predict_page():
    if request.method == 'POST':
        try:
            # Extraer datos del formulario 
            property_data = {
                'calidad_general': int(request.form['calidad_general']),
                'metros_habitables': float(request.form['metros_habitables']),
                'coches_garaje': int(request.form['coches_garaje']),
                'area_garaje': float(request.form.get('area_garaje', 0)),
                'metros_totales_sotano': float(request.form.get('metros_totales_sotano', 0)),
                'metros_1ra_planta': float(request.form['metros_1ra_planta']),
                'banos_completos': int(request.form['banos_completos']),
                'total_habitaciones_sobre_suelo': int(request.form['total_habitaciones_sobre_suelo']),
                'ano_construccion': int(request.form['ano_construccion']),
                'ano_renovacion': int(request.form.get('ano_renovacion', 0)),
                'area_revestimiento_mamposteria': float(request.form.get('area_revestimiento_mamposteria', 0)),
                'chimeneas': int(request.form.get('chimeneas', 0)),
                'metros_acabados_sotano_1': float(request.form.get('metros_acabados_sotano_1', 0)),
                'frente_lote': float(request.form.get('frente_lote', 0)),
                'calidad_exterior': request.form['calidad_exterior'],
                'calidad_cocina': request.form['calidad_cocina'],
                'calidad_sotano': request.form['calidad_sotano'],
                'acabado_garaje': request.form['acabado_garaje'],
                'aire_acondicionado_central': request.form['aire_acondicionado_central'],
                'calidad_chimenea': request.form['calidad_chimenea'],
                'cimentacion': request.form['cimentacion'],
                'tipo_garaje': request.form['tipo_garaje'],
                'tipo_revestimiento_mamposteria': request.form['tipo_revestimiento_mamposteria'],
                'calidad_calefaccion': request.form['calidad_calefaccion'],
                'vecindario': request.form['vecindario']
            }
            
            # Realizar la predicción con el modelo
            prediction_result = predict_house_price(property_data)
            
            # Guardar en base de datos
            property_obj = Property(**property_data)
            property_obj.save()
            prediction = Prediction(
                property_id=property_obj.id,
                predicted_value=prediction_result
            ).save()
            
            flash("¡Predicción completada con éxito!", "success")
            return render_template('predict.html', 
                                  prediction_saved=True,
                                  prediction_result=prediction_result,
                                  input_data=property_data,
                                  form_data={})
                                  
        except Exception as e:
            log.error(f"Error al procesar predicción: {e}", exc_info=True)
            flash(f"Error al procesar la predicción: {str(e)}", "danger")
            return render_template('predict.html', prediction_saved=False, form_data=request.form)
    
    # Si es GET, mostrar el formulario vacío
    return render_template('predict.html', prediction_saved=False, form_data={})