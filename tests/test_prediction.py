import pytest
import numpy as np
import pandas as pd
from unittest.mock import patch, MagicMock

def test_end_to_end_prediction(app, sample_form_data, mock_db):
    """
    Test completo del proceso de predicción utilizando el modelo real.
    Este test verifica:
    1. La carga del modelo real
    2. El procesamiento de datos del formulario
    3. La generación de una predicción válida
    """
    with app.app_context():
        from app.model_loader import load_model_on_startup, get_prediction_model
        
        # Carga el modelo real
        load_model_on_startup(app)
        
        # Verificar que el modelo está cargado correctamente
        model_dict = get_prediction_model()
        assert model_dict is not None
        assert 'modelo' in model_dict
        
        # Imprimir información sobre las features para diagnóstico
        print(f"\nVariables en el modelo:")
        print(f"Numéricas: {len(model_dict['variables_numericas'])}")
        print(f"Categóricas originales: {len(model_dict['variables_categoricas_originales'])}")
        print(f"Categóricas codificadas: {len(model_dict['variables_categoricas_encoded'])}")
        
        # Mocks necesarios para evitar acceder a la base de datos real
        with patch('app.utils.db_utils.execute_query'):
            with patch('app.utils.db_utils.insert_and_get_id', return_value=1):
                # Crear un cliente de prueba
                client = app.test_client()
                
                # Hacer una solicitud POST con datos de formulario
                response = client.post('/predict', data=sample_form_data)
                
                # Verificar que la respuesta es exitosa
                assert response.status_code == 200
                
                # Verificar que la respuesta contiene el resultado de la predicción
                # (El texto exacto dependerá de cómo renderices la respuesta)
                assert b'Precio Estimado' in response.data or b'prediction_result' in response.data
                
                # Opcional: Imprimir parte de la respuesta para verificar visualmente
                print("\nRespuesta de la solicitud POST a /predict:")
                print(response.data[:500])  # Primeros 500 caracteres

def test_manual_prediction_process(app, sample_form_data):
    """
    Test que emula manualmente el proceso de predicción para validar
    cada paso del proceso sin depender de la ruta HTTP.
    """
    with app.app_context():
        from app.model_loader import load_model_on_startup, get_prediction_model
        import pandas as pd
        
        # Cargar el modelo real
        load_model_on_startup(app)
        model_dict = get_prediction_model()
        
        # Extraer componentes del modelo
        modelo = model_dict['modelo']
        scaler = model_dict.get('scaler')
        variables_numericas = model_dict['variables_numericas']
        variables_categoricas = model_dict['variables_categoricas_originales']
        variables_ohe = model_dict['variables_categoricas_encoded']
        transformacion_log = model_dict.get('transformacion_log', False)
        
        print(f"\nComponentes del modelo:")
        print(f"Variables numéricas: {variables_numericas}")
        print(f"Variables categóricas: {variables_categoricas}")
        print(f"Transformación log: {transformacion_log}")
        
        # 1. Procesar variables numéricas
        # Crear un mapping para convertir nombres de formulario a nombres internos
        # Esto es un mapeo simplificado, ajústalo según tus datos reales
        form_to_internal = {
            'CalidadGeneral': 'CalidadGeneral',
            'MetrosHabitables': 'MetrosHabitables',
            'CochesGaraje': 'CochesGaraje',
            'ÁreaGaraje': 'ÁreaGaraje',
            'MetrosTotalesSótano': 'MetrosTotalesSótano',
            'Metros1raPlanta': 'Metros1raPlanta',
            'BañosCompletos': 'BañosCompletos',
            'TotalHabitacionesSobreSuelo': 'TotalHabitacionesSobreSuelo',
            'AñoConstrucción': 'AñoConstrucción',
            'AñoRenovación': 'AñoRenovación',
            'ÁreaRevestimientoMampostería': 'ÁreaRevestimientoMampostería',
            'Chimeneas': 'Chimeneas',
            'MetrosAcabadosSótano1': 'MetrosAcabadosSótano1',
            'FrenteLote': 'FrenteLote'
        }
        
        # Extraer y convertir variables numéricas
        numeric_values = {}
        for form_key, internal_key in form_to_internal.items():
            if form_key in sample_form_data and internal_key in variables_numericas:
                try:
                    numeric_values[internal_key] = float(sample_form_data[form_key])
                except (ValueError, TypeError):
                    pass  # Ignorar conversiones inválidas en este test
        
        # Crear DataFrame numérico en el orden correcto
        numeric_df = pd.DataFrame([{var: numeric_values.get(var, 0) for var in variables_numericas}])
        
        # 2. Aplicar escalado si existe scaler
        if scaler:
            numeric_scaled = scaler.transform(numeric_df)
            print(f"Datos numéricos escalados: {numeric_scaled}")
        else:
            numeric_scaled = numeric_df.values
            print("No se encontró scaler, usando valores sin escalar")
        
        # 3. Procesar variables categóricas
        # Crear un DataFrame con variables categóricas
        categorical_data = {}
        for var in variables_categoricas:
            if var in sample_form_data:
                categorical_data[var] = [sample_form_data[var]]
            else:
                # Valor predeterminado si no está en los datos del formulario
                categorical_data[var] = ['Unknown']
        
        categorical_df = pd.DataFrame(categorical_data)
        
        # 4. Aplicar one-hot encoding
        cat_encoded = pd.get_dummies(categorical_df, columns=variables_categoricas, drop_first=False)
        
        # Asegurar que todas las columnas esperadas estén presentes
        all_cols = set(cat_encoded.columns)
        missing_cols = [col for col in variables_ohe if col not in all_cols]
        
        if missing_cols:
            print(f"Columnas faltantes en la codificación OHE: {missing_cols}")
            # Añadir columnas faltantes con valor 0
            for col in missing_cols:
                cat_encoded[col] = 0
        
        # Reordenar columnas según lo esperado por el modelo
        cat_encoded_reordered = cat_encoded.reindex(columns=variables_ohe, fill_value=0)
        
        # 5. Combinar datos numéricos y categóricos en un DataFrame
        # Primero convertimos los datos numéricos escalados de vuelta a un DataFrame
        numeric_df = pd.DataFrame([numeric_scaled[0]], columns=variables_numericas)
        
        # Combinamos con las variables categóricas
        all_features_df = pd.concat([numeric_df, cat_encoded_reordered], axis=1)
        
        print(f"Forma final de features DataFrame: {all_features_df.shape}")
        
        # 6. Hacer predicción usando el DataFrame con nombres de columnas
        prediction = modelo.predict(all_features_df)
        raw_prediction = prediction[0]
        
        # 7. Aplicar transformación inversa si es necesario
        if transformacion_log:
            final_prediction = np.expm1(raw_prediction)
        else:
            final_prediction = raw_prediction
        
        # Verificar que la predicción es un número positivo
        assert isinstance(final_prediction, (int, float))
        assert final_prediction > 0
        
        # Imprimir resultado
        print(f"\nPredicción manual exitosa:")
        print(f"Predicción bruta: {raw_prediction}")
        print(f"Predicción final: ${final_prediction:,.2f}")