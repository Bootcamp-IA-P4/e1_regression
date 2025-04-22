# app/routes.py (Versión Completa, Corregida para Ames con Reordenado)

from flask import (
    Blueprint, render_template, request, flash, url_for, redirect # Mantenemos url_for/redirect
    # current_app, jsonify no son necesarios para este código específico
)
import pandas as pd
import numpy as np
from app.model_loader import get_prediction_model # Devuelve dict de Ames
from app.models.property import Property          # Necesaria indirectamente
from app.models.prediction import Prediction
import logging
import traceback # Para logging detallado opcional

log = logging.getLogger(__name__)

main_bp = Blueprint('main', __name__, template_folder='templates', static_folder='static')

@main_bp.route('/')
def index():
    """Página principal: Muestra formulario y lista de predicciones recientes."""
    recent_predictions_data = []
    try:
        recent_predictions_data = Prediction.get_recent_with_property(limit=10)
    except Exception as e:
        log.exception("Error al obtener predicciones recientes para la página principal.")
        flash('No se pudieron cargar las predicciones recientes.', 'error')
    return render_template('index.html', recent_predictions=recent_predictions_data)


@main_bp.route('/predict', methods=['GET', 'POST'])
def predict_page():
    """Página para realizar una nueva predicción (PARA AMES HOUSING)."""

    # Mapeo Nombres Formulario -> Nombres Internos/DB (Snake Case)
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
    # Listas Internas (Snake Case)
    numeric_int_keys = ['calidad_general', 'coches_garaje', 'banos_completos', 'total_habitaciones_sobre_suelo',
                        'chimeneas', 'ano_construccion', 'ano_renovacion']
    numeric_float_keys = ['metros_habitables', 'area_garaje', 'metros_totales_sotano', 'metros_1ra_planta',
                          'area_revestimiento_mamposteria', 'metros_acabados_sotano_1', 'frente_lote']
    categorical_keys = ['calidad_exterior', 'calidad_cocina', 'calidad_sotano', 'acabado_garaje',
                        'aire_acondicionado_central', 'calidad_chimenea', 'cimentacion', 'tipo_garaje',
                        'tipo_revestimiento_mamposteria', 'calidad_calefaccion', 'vecindario']
    numeric_cols_snake_case = numeric_int_keys + numeric_float_keys
    categorical_cols_snake_case = categorical_keys

    if request.method == 'POST':
        form_data = request.form.to_dict()
        property_data_for_db = {}

        try:
            # 1. Validar y Convertir Tipos (Genera property_data_for_db con snake_case)
            log.debug("Validando y convirtiendo datos del formulario para Ames...")
            for form_key, internal_key in feature_mapping_ames.items():
                value_str = form_data.get(form_key)
                if value_str is None or value_str.strip() == '':
                    if internal_key in ['frente_lote', 'area_revestimiento_mamposteria', 'area_garaje', 'metros_totales_sotano', 'metros_acabados_sotano_1', 'coches_garaje', 'chimeneas']: # Añadidos los 0 si aplica
                        value_str = "0"
                    else:
                         raise ValueError(f"El campo '{form_key}' es requerido.")
                value_str = value_str.strip()
                converted_value = None
                try:
                    if internal_key in numeric_int_keys: converted_value = int(value_str)
                    elif internal_key in numeric_float_keys: converted_value = float(value_str)
                    elif internal_key in categorical_keys: converted_value = value_str
                    else: raise RuntimeError(f"Clave interna no clasificada: {internal_key}")
                    if isinstance(converted_value, float) and not np.isfinite(converted_value):
                        raise ValueError(f"Valor numérico inválido para '{form_key}'")
                    property_data_for_db[internal_key] = converted_value
                except ValueError as ve:
                    raise ValueError(f"Error en campo '{form_key}': {ve}") from ve
            log.info("Validación y conversión inicial completada.")


            # 2. Preparar datos para el modelo ML
            log.debug("Obteniendo componentes del modelo Ames...")
            model_components = get_prediction_model()
            ames_model = model_components.get('modelo')
            scaler = model_components.get('scaler')
            variables_numericas_pkl = model_components.get('variables_numericas') # Nombres (PascalCase?) y ORDEN del PKL
            variables_categoricas_pkl = model_components.get('variables_categoricas_originales') # Nombres (PascalCase?) y ORDEN del PKL
            variables_ohe_pkl = model_components.get('variables_categoricas_encoded')
            transformacion_log_target = model_components.get('transformacion_log', False) # Para el PRECIO

            if not all([ames_model, scaler, variables_numericas_pkl, variables_categoricas_pkl, variables_ohe_pkl]):
                log.error("Faltan componentes esenciales del modelo Ames en el archivo PKL.")
                raise RuntimeError("Componentes esenciales del modelo Ames no encontrados.")
            log.debug(f"Modelo PKL espera numéricas (y orden): {variables_numericas_pkl}")
            log.debug(f"Modelo PKL espera categóricas originales (y orden): {variables_categoricas_pkl}")


            # 2b. Crear DataFrame inicial (con nombres snake_case)
            initial_df = pd.DataFrame([property_data_for_db])

            # 2c. Preprocesamiento: Seleccionar, Renombrar, REORDENAR, Transformar

            # -> Seleccionar columnas snake_case
            try:
                df_numeric_snake = initial_df[numeric_cols_snake_case].copy()
                df_categorical_snake = initial_df[categorical_cols_snake_case].copy()
            except KeyError as e:
                log.error(f"Error seleccionando cols snake_case. Falta {e}", exc_info=True)
                raise RuntimeError(f"Error interno: Configuración de cols snake_case incorrecta ({e}).")

            # -> Renombrar a nombres del PKL (PascalCase/Original?)
            if len(numeric_cols_snake_case) != len(variables_numericas_pkl) or \
               len(categorical_cols_snake_case) != len(variables_categoricas_pkl):
                raise RuntimeError("Inconsistencia en número de columnas (snake vs PKL).")
            rename_dict_num = dict(zip(numeric_cols_snake_case, variables_numericas_pkl))
            rename_dict_cat = dict(zip(categorical_cols_snake_case, variables_categoricas_pkl))
            df_numeric_renamed = df_numeric_snake.rename(columns=rename_dict_num)
            df_categorical_renamed = df_categorical_snake.rename(columns=rename_dict_cat)


            # ---> ¡¡CORRECCIÓN CRUCIAL: REORDENAR ANTES DE SCALER!! <---
            log.debug(f"Columnas numéricas ANTES de reordenar para scaler: {df_numeric_renamed.columns.tolist()}")
            try:
                # Reordenar df_numeric_renamed usando el orden EXACTO de variables_numericas_pkl
                df_numeric_reordered_for_scaler = df_numeric_renamed[variables_numericas_pkl]
                log.debug(f"Columnas numéricas DESPUÉS de reordenar para scaler: {df_numeric_reordered_for_scaler.columns.tolist()}")
            except KeyError as e:
                log.error(f"Error reordenando columnas numéricas para scaler. Falta {e}", exc_info=True)
                raise RuntimeError(f"Error interno: Falta columna numérica {e} esperada por el scaler.")


            # -> Aplicar Log a FEATURES si es necesario (sobre df reordenado)
            #    ¡DEBES VERIFICAR TU NOTEBOOK! Si hiciste log(features), descomenta y adáptalo.
            # if model_components.get('log_features', False):
            #    log.warning("Aplicando log1p a features numéricas reordenadas...")
            #    df_numeric_reordered_for_scaler = np.log1p(df_numeric_reordered_for_scaler)


            # -> Escalar (¡Usando el DF reordenado!)
            log.debug(f"Escalando variables numéricas reordenadas...")
            df_numeric_scaled_array = scaler.transform(df_numeric_reordered_for_scaler)
            df_numeric_scaled = pd.DataFrame(df_numeric_scaled_array, index=initial_df.index, columns=variables_numericas_pkl) # Mantener nombres y orden del PKL
            # -> Log para VER los valores escalados:
            log.debug(f"DF numérico escalado (.head()):\n{df_numeric_scaled.head().to_string()}")


            # -> OHE (sobre df categórico renombrado)
            log.debug("Aplicando OHE a variables categóricas renombradas...")
            # ¡Verificar drop_first según entrenamiento!
            df_categorical_encoded = pd.get_dummies(df_categorical_renamed, columns=variables_categoricas_pkl, drop_first=False)
            log.debug("Reindexando columnas OHE...")
            # Reindexar para asegurar todas las columnas OHE del entrenamiento
            df_categorical_encoded = df_categorical_encoded.reindex(columns=variables_ohe_pkl, fill_value=0)


            # -> Combinar y preparar final para el modelo
            df_predict = pd.concat([df_numeric_scaled, df_categorical_encoded], axis=1)
            expected_cols_model = variables_numericas_pkl + variables_ohe_pkl

            missing_cols = set(expected_cols_model) - set(df_predict.columns)
            extra_cols = set(df_predict.columns) - set(expected_cols_model)
            if missing_cols or extra_cols:
                log.error(f"Discrepancia columnas OHE finales! Faltan: {missing_cols}, Extras: {extra_cols}")
                raise RuntimeError("Error en la preparación final del DataFrame OHE.")
            # Reordenar final por si acaso el modelo Ridge es sensible
            df_predict = df_predict[expected_cols_model]
            log.debug(f"DataFrame final ({df_predict.shape}) listo para modelo.")
            # -> Log para VER lo que entra al modelo:
            log.debug(f"Datos ENVIADOS al modelo (.head()):\n{df_predict.head().to_string()}")


            # 3. Predecir
            log.debug("Realizando predicción con modelo Ames...")
            prediction_result_raw = ames_model.predict(df_predict)
            predicted_value_raw = float(prediction_result_raw[0])
            # -> Log para VER la predicción raw:
            log.info(f"Predicción obtenida (escala raw/log Ames): {predicted_value_raw}")
            log.critical(f"!!! VALOR RAW DE PREDICCIÓN (ANTES DE INVERSA): {predicted_value_raw}")


            # 4. Transformación Inversa del Precio
            predicted_value_dollars = predicted_value_raw
            if transformacion_log_target:
                # ---- ¡¡¡ IMPORTANTE: VERIFICA ESTA FUNCIÓN !!! ----
                # Usa np.expm1 si hiciste np.log1p(precio)
                # Usa np.exp si hiciste np.log(precio)
                inverse_func = np.expm1
                # ---- ¡¡¡ ------------------------------------ !!! ----
                log.info(f"Aplicando {inverse_func.__name__} a predicción raw del precio...")
                try:
                    predicted_value_dollars = inverse_func(predicted_value_raw)
                except Exception as e:
                     log.error(f"Error en {inverse_func.__name__}: {e}. Usando valor raw.", exc_info=True)
                     flash('Advertencia: Error convirtiendo predicción a $.', 'warning')
                     predicted_value_dollars = predicted_value_raw

            if not np.isfinite(predicted_value_dollars):
                 log.warning(f"Resultado inversa no finito ({predicted_value_dollars}). Usando valor raw.")
                 flash('Advertencia: Resultado inválido. Mostrando valor transformado.', 'warning')
                 predicted_value_dollars = predicted_value_raw
            else:
                 # Redondear a 2 decimales para dólares
                 predicted_value_dollars = round(float(predicted_value_dollars), 2)

            log.info(f"Predicción final (dólares Ames): {predicted_value_dollars:.2f}")


            # 5. Guardar Propiedad y Predicción
            log.debug(f"Guardando propiedad Ames con datos (snake_case): {property_data_for_db}")
            saved_property, saved_prediction = Prediction.create_from_data(
                property_data=property_data_for_db,
                prediction_data={'predicted_value': predicted_value_dollars} # VALOR EN DÓLARES
            )

            if not saved_property or not saved_prediction:
                flash('Error al guardar los resultados en la base de datos.', 'error')
                return render_template('predict.html', form_data=form_data, error_message='No se pudo guardar.'), 500
            else:
                log.info(f'Guardado OK (Propiedad ID: {saved_property.id}, Predicción ID: {saved_prediction.id}).')
                flash(f'Predicción realizada y guardada (Propiedad ID: {saved_property.id}, Predicción ID: {saved_prediction.id}).', 'success')
                # Pasar valor en dólares y datos validados
                return render_template('predict.html',
                                       prediction_result=predicted_value_dollars,
                                       input_data=property_data_for_db,
                                       prediction_saved=True)

        # --- Bloques Except ---
        except ValueError as e: # Errores de validación / conversión de tipos
            log.warning(f"Error de Validación de Datos: {e}", exc_info=False)
            # traceback.print_exc() # Descomenta para depuración más profunda si es necesario
            flash(f'Error en los datos ingresados: {e}', 'warning')
            return render_template('predict.html', form_data=form_data), 400
        except RuntimeError as e: # Errores nuestros (config, modelo no carga, preproc mismatch)
            log.error(f"Error Crítico de Ejecución: {e}", exc_info=True)
            flash(f'Error interno del servidor. Contacte al administrador.', 'danger')
            return render_template('predict.html', form_data=form_data), 500
        except KeyError as e: # Faltan columnas
             log.exception(f"Error de Clave (KeyError) procesando datos: {e}")
             flash(f'Error interno: Falta un dato esperado ({e}). Contacte al administrador.', 'danger')
             return render_template('predict.html', form_data=form_data), 500
        except Exception as e: # Otros errores inesperados (DB, etc.)
             log.exception("Error Inesperado en /predict [POST]")
             flash(f'Ocurrió un error inesperado ({type(e).__name__}). Contacte al administrador.', 'danger')
             return render_template('predict.html', form_data=form_data), 500

    # --- Método GET ---
    return render_template('predict.html', form_data={})