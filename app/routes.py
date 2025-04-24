from flask import (
    Blueprint, render_template, request, flash
    )
import pandas as pd
import numpy as np
from app.model_loader import get_prediction_model
from app.models.prediction import Prediction
import logging

log = logging.getLogger(__name__)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

main_bp = Blueprint('main', __name__, template_folder='templates', static_folder='static')

@main_bp.route('/')
def index():
    recent_predictions_data = []
    try:
        recent_predictions_data = Prediction.get_recent_with_property(limit=10)
    except Exception as e:
        log.exception("Error al obtener predicciones recientes para la página principal.")
        flash('No se pudieron cargar las predicciones recientes.', 'error')
    return render_template('index.html', recent_predictions=recent_predictions_data)


@main_bp.route('/predict', methods=['GET', 'POST'])
def predict_page():
    """Página para realizar una nueva predicción (AMES - SIN ESCALAR - Simplificado)."""

    # Mapeo Formulario (PascalCase) -> Interno (snake_case)
    # ¡¡ASEGÚRATE que las claves (PascalCase) coinciden EXACTAMENTE con las del form HTML!!
    # ¡¡Y que los valores (snake_case) coinciden con los attrs de Property/DB!!
    feature_mapping_ames = {
        'CalidadGeneral': 'calidad_general', 'MetrosHabitables': 'metros_habitables',
        'CochesGaraje': 'coches_garaje', 'ÁreaGaraje': 'area_garaje', 'MetrosTotalesSótano': 'metros_totales_sotano',
        'Metros1raPlanta': 'metros_1ra_planta', 'BañosCompletos': 'banos_completos', 'TotalHabitacionesSobreSuelo': 'total_habitaciones_sobre_suelo',
        'AñoConstrucción': 'ano_construccion', 'AñoRenovación': 'ano_renovacion', 'ÁreaRevestimientoMampostería': 'area_revestimiento_mamposteria',
        'Chimeneas': 'chimeneas', 'MetrosAcabadosSótano1': 'metros_acabados_sotano_1', 'FrenteLote': 'frente_lote',
        'CalidadExterior': 'calidad_exterior', 'CalidadCocina': 'calidad_cocina', 'CalidadSótano': 'calidad_sotano',
        'AcabadoGaraje': 'acabado_garaje', 'AireAcondicionadoCentral': 'aire_acondicionado_central', 'CalidadChimenea': 'calidad_chimenea',
        'Cimentación': 'cimentacion', 'TipoGaraje': 'tipo_garaje', 'TipoRevestimientoMampostería': 'tipo_revestimiento_mamposteria',
        'CalidadCalefacción': 'calidad_calefaccion', 'Vecindario': 'vecindario'
    }
    # Listas Internas (Snake Case) - SOLO para validación inicial de tipos
    numeric_int_keys = ['calidad_general', 'coches_garaje', 'banos_completos', 'total_habitaciones_sobre_suelo', 'chimeneas', 'ano_construccion', 'ano_renovacion']
    numeric_float_keys = ['metros_habitables', 'area_garaje', 'metros_totales_sotano', 'metros_1ra_planta', 'area_revestimiento_mamposteria', 'metros_acabados_sotano_1', 'frente_lote']
    categorical_keys = ['calidad_exterior', 'calidad_cocina', 'calidad_sotano', 'acabado_garaje', 'aire_acondicionado_central', 'calidad_chimenea', 'cimentacion', 'tipo_garaje', 'tipo_revestimiento_mamposteria', 'calidad_calefaccion', 'vecindario']

    if request.method == 'POST':
        form_data = request.form.to_dict()
        property_data_for_db = {} # Datos validados snake_case

        try:
            # 1. Validar y Convertir Tipos
            log.debug("Validando y convirtiendo datos del formulario...")
            for form_key, internal_key in feature_mapping_ames.items():
                value_str = form_data.get(form_key)
                if value_str is None or value_str.strip() == '':
                    # Aplicar default 0 solo a columnas que lo permitan/requieran
                    if internal_key in [
                        'frente_lote', 'area_revestimiento_mamposteria', 'area_garaje',
                        'metros_totales_sotano', 'metros_acabados_sotano_1', 'coches_garaje', 'chimeneas']:
                        value_str = "0"
                    elif internal_key in categorical_keys:
                        raise ValueError(f"El campo '{form_key}' es requerido.")
                    else:
                        raise ValueError(f"El campo '{form_key}' es requerido.")
                value_str = value_str.strip()
                try:
                    if internal_key in numeric_int_keys:
                        converted_value = int(value_str)
                    elif internal_key in numeric_float_keys:
                        converted_value = float(value_str)
                    elif internal_key in categorical_keys:
                        converted_value = value_str
                    else:
                        raise RuntimeError(f"Clave interna no clasificada: {internal_key}")
                    # Validación extra para floats
                    if isinstance(converted_value, float) and not np.isfinite(converted_value):
                        raise ValueError("Valor numérico inválido (NaN/inf)")
                    property_data_for_db[internal_key] = converted_value
                except ValueError as ve:
                    # Error específico en la conversión de tipo
                    raise ValueError(f"Error de formato en campo '{form_key}': '{value_str}' no es un valor válido.") from ve
            log.info("Validación inicial OK.")
            log.debug(f"Datos convertidos (snake_case): {property_data_for_db}")


            # 2. Preparar datos para el modelo ML (Simplificado)
            log.debug("Obteniendo componentes del modelo...")
            model_components = get_prediction_model()
            ames_model = model_components.get('modelo')
            scaler = model_components.get('scaler')  # <-- Asegúrate de cargar el scaler
            variables_numericas_pkl = model_components.get('variables_numericas')       # Nombres PascalCase (del PKL)
            variables_categoricas_pkl = model_components.get('variables_categoricas_originales') # Nombres PascalCase (del PKL)
            variables_ohe_pkl = model_components.get('variables_categoricas_encoded') # Nombres OHE (del PKL)
            transformacion_log_target = model_components.get('transformacion_log', False)

            # Validar componentes
            if not all([ames_model, variables_numericas_pkl, variables_categoricas_pkl, variables_ohe_pkl]):
                 log.error("Faltan componentes esenciales en PKL.")
                 raise RuntimeError("Componentes esenciales del modelo no encontrados.")

            log.debug(f"PKL Numéricas Esperadas (Orden): {variables_numericas_pkl}")
            log.debug(f"PKL Categóricas Originales (Orden): {variables_categoricas_pkl}")
            log.debug(f"PKL Categóricas OHE (Orden): {variables_ohe_pkl}")

            # --- Crear mapeo PKL(PascalCase) -> DB(snake_case) ---
            # Se usa el feature_mapping_ames original, que ya mapea Pascal -> Snake
            # ¡Solo necesitamos verificar que cubra todas las vars del PKL!
            map_pkl_to_snake = feature_mapping_ames
            log.debug(f"Usando mapeo (PKL/Form -> snake): {map_pkl_to_snake}")

            # Verificar cobertura del mapeo
            missing_maps_num = [v for v in variables_numericas_pkl if v not in map_pkl_to_snake]
            missing_maps_cat = [v for v in variables_categoricas_pkl if v not in map_pkl_to_snake]
            if missing_maps_num or missing_maps_cat:
                log.error(f"¡Mapeo Incompleto! Falta mapeo para: Num={missing_maps_num}, Cat={missing_maps_cat}")
                raise RuntimeError("Error crítico en configuración del mapeo PKL->snake.")


            # --- A. Preparar Lista Numérica Final (Ordenada según PKL) ---
            numeric_values_final_ordered = []
            log.debug("Construyendo lista numérica final ordenada...")
            for pkl_num_var in variables_numericas_pkl: # Iterar sobre nombres PKL
                snake_case_var = map_pkl_to_snake.get(pkl_num_var) # Obtener nombre snake_case
                if snake_case_var is None:
                    # Esta verificación es doble, pero segura
                    raise RuntimeError(f"Mapeo PKL->snake falta para '{pkl_num_var}' (numérica)")

                value = property_data_for_db.get(snake_case_var) # Obtener valor validado
                if value is None:
                    raise ValueError(f"Valor nulo inesperado para '{snake_case_var}' (PKL: '{pkl_num_var}')")
                numeric_values_final_ordered.append(value)
                log.debug(f"  -> Añadido Num: '{pkl_num_var}' (valor: {value})")
            log.debug(f"Lista Numérica Final Ordenada ({len(numeric_values_final_ordered)}): {numeric_values_final_ordered}")

            # --- A.1. ESCALAR variables numéricas ---
            # Convierte a DataFrame para aplicar el scaler
            import pandas as pd
            X_num_df = pd.DataFrame([dict(zip(variables_numericas_pkl, numeric_values_final_ordered))])
            if scaler is not None:
                X_num_scaled = scaler.transform(X_num_df)
                log.debug(f"Numéricas escaladas: {X_num_scaled}")
                numeric_values_final_ordered = X_num_scaled[0].tolist()
            else:
                log.warning("No se encontró scaler en el modelo. Usando valores sin escalar.")


            # --- B. Preparar DataFrame Categórico (Nombres PKL) ---
            categorical_data_for_ohe = {}
            log.debug("Construyendo dict categórico para OHE (claves=PKL)...")
            for pkl_cat_var in variables_categoricas_pkl: # Iterar sobre nombres PKL
                snake_case_var = map_pkl_to_snake.get(pkl_cat_var) # Obtener nombre snake_case
                if snake_case_var is None:
                     raise RuntimeError(f"Mapeo PKL->snake falta para '{pkl_cat_var}' (categórica)")
                value = property_data_for_db.get(snake_case_var) # Obtener valor validado
                if value is None:
                     raise ValueError(f"Valor categórico nulo inesperado para '{snake_case_var}' (PKL: '{pkl_cat_var}')")
                categorical_data_for_ohe[pkl_cat_var] = [value] # Clave es nombre PKL
                log.debug(f"  -> Añadido Cat: '{pkl_cat_var}' (valor: {value})")

            # Crear DataFrame directamente con nombres PKL
            df_categorical_renamed = pd.DataFrame.from_dict(categorical_data_for_ohe)
            log.debug(f"DataFrame Categórico (claves=PKL) listo para OHE:\n{df_categorical_renamed.to_string()}")


            # --- C. Aplicar OHE y Reindex ---
            # --- ¡¡¡ CONFIRMA drop_first CON TU ENTRENAMIENTO !!! ---
            drop_first_ohe = False # O True
            log.warning(f"Usando drop_first={drop_first_ohe} para OHE.")
            try:
                df_categorical_encoded = pd.get_dummies(df_categorical_renamed,
                                                        columns=variables_categoricas_pkl, # Columnas a codificar (ya tienen nombre PKL)
                                                        drop_first=drop_first_ohe,
                                                        dtype=int)
                log.debug(f"Columnas OHE (ANTES reindex): {df_categorical_encoded.columns.tolist()}")
                df_categorical_encoded_reindexed = df_categorical_encoded.reindex(columns=variables_ohe_pkl, fill_value=0)
                log.debug(f"Columnas OHE (DESPUÉS reindex): {df_categorical_encoded_reindexed.columns.tolist()}")
            except Exception as e:
                 log.exception("Error OHE/Reindex.")
                 raise RuntimeError(f"Error en OHE/Reindex: {e}")

            # Convertir a lista
            categorical_values_final_ordered = df_categorical_encoded_reindexed.iloc[0].tolist()
            log.debug(f"Lista Categórica OHE Final ({len(categorical_values_final_ordered)}): {categorical_values_final_ordered}")


            # --- D. Combinar Datos Finales ---
            final_features_list = numeric_values_final_ordered + categorical_values_final_ordered
            log.debug(f"Lista combinada final ({len(final_features_list)}): {final_features_list}")
            final_features_array = np.array([final_features_list])
            log.debug(f"Array NumPy final (shape {final_features_array.shape}):\n{final_features_array}")

            # Verificar #features
            expected_feature_count = len(variables_numericas_pkl) + len(variables_ohe_pkl)
            if final_features_array.shape[1] != expected_feature_count:
                log.error(f"Discrepancia final #features! Esperado: {expected_feature_count}, Obtenido: {final_features_array.shape[1]}")
                raise RuntimeError("Error en número final de features.")
            log.info(f"Preparación de datos OK. Shape final: {final_features_array.shape}")


            # 3. Predecir
            log.debug("Realizando predicción...")
            prediction_result_raw = ames_model.predict(final_features_array)
            predicted_value_raw = float(prediction_result_raw[0])
            log.info(f"Predicción RAW (SIN ESCALAR): {predicted_value_raw}")
            log.critical(f"!!! VALOR RAW PREDICCIÓN: {predicted_value_raw}")


            # 4. Transformación Inversa
            predicted_value_dollars = predicted_value_raw
            if transformacion_log_target:
                inverse_func = np.expm1 # Asumiendo log1p
                log.info(f"Aplicando '{inverse_func.__name__}'...")
                try:
                    predicted_value_transformed = inverse_func(predicted_value_raw)
                    if not np.isfinite(predicted_value_transformed):
                        log.warning(f"Inversa no finita. Usando raw {predicted_value_raw:.2f}.")
                        flash(f'Advertencia: Cálculo inválido. Mostrando base {predicted_value_raw:.2f}.', 'warning')
                        predicted_value_dollars = round(predicted_value_raw, 2)
                    else:
                        predicted_value_dollars = round(float(predicted_value_transformed), 2)
                except OverflowError:
                    log.error("Overflow en inversa. Usando raw.")
                    flash(f'Advertencia: Desbordamiento. Mostrando base {predicted_value_raw:.2f}.', 'warning')
                except Exception:
                    log.exception("Error en inversa. Usando raw.")
                    flash('Advertencia: Error calculando $.', 'warning')
                    predicted_value_dollars = round(predicted_value_raw, 2)
            else:
                 log.info("No se aplicó log al target.")
                 if not np.isfinite(predicted_value_dollars):
                     log.error(f"Predicción raw no finita ({predicted_value_dollars}).")
                     flash('Error: Predicción base inválida.', 'danger')
                     raise ValueError("Predicción base inválida.")
                 predicted_value_dollars = round(float(predicted_value_dollars), 2)

            log.info(f"Predicción final (dólares, SIN ESCALAR): {predicted_value_dollars:,.2f}")

            # Control de Rango DB
            # --- ¡¡¡ AJUSTA ESTE VALOR A TU COLUMNA `predicted_value` !!! ---
            MAX_DB_VALUE = 9999999999999.99 # Ejemplo: DECIMAL(15,2)
            # -----------------------------------------------------------------
            MIN_DB_VALUE = -MAX_DB_VALUE      # O 0 si no permites negativos
            if not (MIN_DB_VALUE <= predicted_value_dollars <= MAX_DB_VALUE):
                 log.error(f"¡Valor final ({predicted_value_dollars}) fuera de rango DB ({MIN_DB_VALUE} a {MAX_DB_VALUE})!")
                 flash(f"Error: Predicción (${predicted_value_dollars:,.2f}) fuera de rango almacenable.", 'danger')
                 return render_template('predict.html', form_data=form_data), 500 # Error


            # 5. Guardar Propiedad y Predicción
            log.debug(f"Guardando propiedad: {property_data_for_db}")
            saved_property, saved_prediction = Prediction.create_from_data(
                property_data=property_data_for_db,
                prediction_data={'predicted_value': predicted_value_dollars}
            )
            if not saved_property or not saved_prediction:
                log.error(f"Falló guardado DB. Prop: {saved_property is not None}, Pred: {saved_prediction is not None}")
                flash('Error al guardar en base de datos.', 'error')
                return render_template('predict.html', form_data=form_data, error_message='No se pudo guardar.'), 500
            else:
                log.info(f'Guardado DB OK (Prop ID: {saved_property.id}, Pred ID: {saved_prediction.id}).')
                return render_template('predict.html',
                                       prediction_result=predicted_value_dollars,
                                       input_data=property_data_for_db,
                                       prediction_saved=True)

        # --- Bloques Except ---
        except ValueError as e: # Errores Validación / Conversión
            log.warning(f"Error Validación/Formato: {e}", exc_info=False)
            flash(f'Error en datos: {e}', 'warning')
            return render_template('predict.html', form_data=form_data), 400
        except RuntimeError as e: # Errores Internos (PKL, Mapeo, Lógica)
            log.error(f"Error Crítico Interno: {e}", exc_info=True)
            flash('Error interno servidor.', 'danger')
            return render_template('predict.html', form_data=form_data), 500
        except KeyError as e: # Errores específicos de claves faltantes
             log.exception(f"Error Clave (Columna Faltante?): {e}")
             flash(f'Error interno (dato faltante: {e}).', 'danger')
             return render_template('predict.html', form_data=form_data), 500
        except Exception as e: # Otros errores
             log.exception("Error Inesperado POST /predict")
             flash(f'Error inesperado ({type(e).__name__}).', 'danger')
             return render_template('predict.html', form_data=form_data), 500

    # --- Método GET ---
    return render_template('predict.html', form_data={})