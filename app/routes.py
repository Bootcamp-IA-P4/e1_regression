from flask import Blueprint, render_template, request, redirect, url_for, flash
import pandas as pd
from app.model_loader import get_prediction_model
from app.database.models import Prediction

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Obtener las predicciones recientes para mostrar en la página
    try:
        recent_predictions = Prediction.get_recent_predictions(limit=5)
    except Exception as e:
        recent_predictions = []
        flash(f'Error al cargar predicciones recientes: {str(e)}')
        
    return render_template('index.html', recent_predictions=recent_predictions)

@main_bp.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Recoger datos del formulario
        try:
            # Adapta estos campos a las características de tu modelo
            input_data = {
                'MedInc': float(request.form['MedInc']),
                'HouseAge': float(request.form['HouseAge']),
                'AveRooms': float(request.form['AveRooms']),
                'AveBedrms': float(request.form['AveBedrms']),
                'Population': float(request.form['Population']),
                'AveOccup': float(request.form['AveOccup']),
                'Latitude': float(request.form['Latitude']),
                'Longitude': float(request.form['Longitude'])
            }
            
            # Convertir a DataFrame para que coincida con el formato esperado por el modelo
            df = pd.DataFrame([input_data])
            
            # Obtener predicción
            model = get_prediction_model()
            prediction = model.predict(df)[0]
            
            # Guardar la predicción en la base de datos
            prediction_id = Prediction.save(input_data, prediction)
            
            # Renderizar resultado
            return render_template('predict.html', 
                                  prediction=prediction, 
                                  input_data=input_data,
                                  prediction_id=prediction_id)
            
        except Exception as e:
            flash(f'Error en la predicción: {str(e)}')
            return redirect(url_for('main.predict'))
    
    # Si es GET, mostrar formulario
    return render_template('predict.html')