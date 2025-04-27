import os
import pytest
import numpy as np
from unittest.mock import patch

def test_load_model_success(app):
    """Verifica que el modelo real se carga correctamente."""
    with app.app_context():
        from app.model_loader import _load_model_from_path
        
        # Usa la ruta configurada en la aplicación
        model_path = app.config.get('MODEL_PATH')
        
        # Cargar el modelo real
        loaded_dict = _load_model_from_path(model_path)
        
        # Verificar que el diccionario cargado contiene los componentes esperados
        assert 'modelo' in loaded_dict
        assert 'scaler' in loaded_dict
        assert 'variables_numericas' in loaded_dict
        assert 'variables_categoricas_originales' in loaded_dict
        assert 'variables_categoricas_encoded' in loaded_dict
        
        # Verificar que el modelo tiene un método predict
        assert hasattr(loaded_dict['modelo'], 'predict')
        
        # Imprimir información sobre el modelo (opcional)
        print(f"\nModelo cargado correctamente desde: {model_path}")
        print(f"Variables numéricas: {loaded_dict['variables_numericas']}")
        print(f"Variables categóricas: {loaded_dict['variables_categoricas_originales']}")

def test_load_model_on_startup(app):
    """Verifica que load_model_on_startup carga correctamente el modelo real."""
    with app.app_context():
        from app.model_loader import load_model_on_startup, get_prediction_model
        
        # Ejecutar la función que queremos probar
        load_model_on_startup(app)
        
        # Obtener el modelo cargado
        model_dict = get_prediction_model()
        
        # Verificar que el modelo se ha cargado correctamente
        assert model_dict is not None
        assert 'modelo' in model_dict
        assert 'variables_numericas' in model_dict
        
        # Verificar que el modelo tiene un método predict
        assert hasattr(model_dict['modelo'], 'predict')
        
        # Mostrar información sobre el modelo cargado
        print(f"\nModelo cargado correctamente mediante load_model_on_startup")
        print(f"Tipo de modelo: {type(model_dict['modelo'])}")

def test_model_can_predict(app):
    """Verifica que el modelo real puede hacer predicciones usando nombres de columnas correctos."""
    with app.app_context():
        from app.model_loader import load_model_on_startup, get_prediction_model
        import pandas as pd
        
        # Cargar el modelo
        load_model_on_startup(app)
        model_dict = get_prediction_model()
        
        # Obtener información sobre las características esperadas
        num_vars = model_dict['variables_numericas']
        cat_vars_encoded = model_dict['variables_categoricas_encoded']
        
        # Crear un DataFrame con los nombres de columnas correctos
        # Inicializar variables numéricas
        num_data = {var: [7] for var in num_vars}
        
        # Inicializar variables categóricas codificadas
        cat_data = {var: [0] for var in cat_vars_encoded}
        # Activar una característica categórica
        if cat_vars_encoded:
            cat_data[cat_vars_encoded[0]] = [1]
        
        # Combinar en un único DataFrame
        all_features_df = pd.DataFrame({**num_data, **cat_data})
        
        # Asegurarse de que el tamaño coincide con lo esperado
        expected_feature_count = len(num_vars) + len(cat_vars_encoded)
        assert len(all_features_df.columns) == expected_feature_count, \
            f"El número de características no coincide: tiene {len(all_features_df.columns)}, se esperaba {expected_feature_count}"
        
        # Hacer una predicción con el modelo real usando el DataFrame (con nombres de columnas)
        prediction = model_dict['modelo'].predict(all_features_df)
        
        # Verificar que la predicción es un número
        assert isinstance(prediction[0], (int, float))
        
        # Verificar que la predicción está en un rango razonable para precios de vivienda
        assert prediction[0] > 0
        
        # Si hay una transformación logarítmica, aplicar la inversa
        if model_dict.get('transformacion_log', False):
            final_prediction = np.expm1(prediction[0])
        else:
            final_prediction = prediction[0]
        
        # Mostrar la predicción
        print(f"\nPredicción exitosa con el modelo real (usando nombres de columnas):")
        print(f"Número de características: {len(all_features_df.columns)}")
        print(f"Predicción obtenida: ${final_prediction:,.2f}")