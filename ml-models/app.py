import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar la página
st.set_page_config(
    page_title="Predictor de Precios de Casas",
    page_icon="🏠",
    layout="wide"
)

# Cargar el modelo entrenado
@st.cache_resource
def load_model():
    with open('resultados/modelo_regresion.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

model = load_model()

# Cargar datos de importancia de características
@st.cache_data
def load_feature_importance():
    return pd.read_csv('resultados/importancia_caracteristicas.csv')

try:
    feature_importance = load_feature_importance()
except:
    feature_importance = None

# Título y descripción
st.title("🏠 Predictor de Precios de Casas")
st.markdown("""
Esta aplicación predice el precio de una casa basándose en sus características.
Ingresa los valores en el formulario de la izquierda y obtén una predicción instantánea.
""")

# Sidebar con formulario
st.sidebar.header("Ingresa las características de la casa")

# Cargar datos para valores predeterminados
@st.cache_data
def load_data():
    return pd.read_csv('data/train_es_clean.csv')

data = load_data()

# Crear formulario con las características más importantes
# Usaremos un subconjunto de variables para simplificar la interfaz
with st.sidebar.form("input_form"):
    # Variables numéricas más importantes
    calidad_general = st.slider(
        "Calidad General (1-10)", 
        min_value=1, max_value=10, 
        value=7
    )
    
    metros_habitables = st.number_input(
        "Metros Habitables", 
        min_value=50.0, max_value=300.0, 
        value=150.0, step=10.0
    )
    
    metros_sotano = st.number_input(
        "Metros Totales Sótano", 
        min_value=0.0, max_value=200.0, 
        value=80.0, step=10.0
    )
    
    anio_construccion = st.slider(
        "Año de Construcción", 
        min_value=1900, max_value=2023, 
        value=1980
    )
    
    coches_garaje = st.slider(
        "Capacidad del Garaje (coches)", 
        min_value=0, max_value=4, 
        value=2
    )
    
    # Variables categóricas importantes
    vecindario = st.selectbox(
        "Vecindario",
        options=sorted(data['Vecindario'].unique()),
        index=0
    )
    
    tipo_edificio = st.selectbox(
        "Tipo de Edificio",
        options=sorted(data['TipoEdificio'].unique()),
        index=0
    )
    
    zonificacion = st.selectbox(
        "Zonificación",
        options=sorted(data['ZonificaciónMS'].unique()),
        index=0
    )
    
    estilo_casa = st.selectbox(
        "Estilo de Casa",
        options=sorted(data['EstiloCasa'].unique()),
        index=0
    )
    
    submit = st.form_submit_button("Predecir Precio")

# Crear un DataFrame con los datos ingresados
if submit:
    # Crear una copia de la primera fila de los datos originales como plantilla
    input_data = data.iloc[0:1].copy()
    
    # Actualizar con los valores ingresados por el usuario
    input_data['CalidadGeneral'] = calidad_general
    input_data['MetrosHabitables'] = metros_habitables
    input_data['MetrosTotalesSótano'] = metros_sotano
    input_data['AñoConstrucción'] = anio_construccion
    input_data['CochesGaraje'] = coches_garaje
    input_data['Vecindario'] = vecindario
    input_data['TipoEdificio'] = tipo_edificio
    input_data['ZonificaciónMS'] = zonificacion
    input_data['EstiloCasa'] = estilo_casa
    
    # Eliminar la columna de precio (variable objetivo)
    if 'PrecioVenta' in input_data.columns:
        input_data = input_data.drop('PrecioVenta', axis=1)
    
    # Realizar la predicción
    prediction = model.predict(input_data)[0]
    
    # Mostrar resultado
    col1, col2 = st.columns(2)
    with col1:
        st.header("Resultado de la Predicción")
        st.markdown(f"""
        ## Precio Estimado: ${prediction:,.2f}
        
        *Nota: Este es un precio estimado basado en las características proporcionadas.*
        """)
    
    with col2:
        st.header("Interpretación")
        st.markdown(f"""
        - Una casa con **calidad general de {calidad_general}/10**
        - **{metros_habitables:.1f} m²** habitables
        - Construida en **{anio_construccion}**
        - En el vecindario **{vecindario}**
        - Tipo de edificio: **{tipo_edificio}**
        """)

# Mostrar métricas del modelo y visualizaciones
st.header("Rendimiento del Modelo")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Métricas de Evaluación")
    st.markdown("""
    El modelo fue evaluado con las siguientes métricas:
    
    | Métrica | Valor en Test |
    | ------- | ------------- |
    | R² | 0.82 |
    | RMSE | 28,569.32 |
    | MAE | 19,384.45 |
    
    *Estos valores son aproximados y pueden variar según la ejecución específica del modelo.*
    """)

with col2:
    st.subheader("Predicciones vs Valores Reales")
    st.image("resultados/predicciones_vs_reales.png", use_column_width=True)

# Mostrar importancia de características si está disponible
if feature_importance is not None:
    st.header("Características Más Importantes")
    st.image("resultados/top_20_caracteristicas.png", use_column_width=True)
    
    with st.expander("Ver tabla completa de importancia de características"):
        st.dataframe(feature_importance)

# Notas finales
st.markdown("""
---
### Sobre el Modelo
Este predictor utiliza un modelo de regresión lineal entrenado con datos de casas. 
Las predicciones son más precisas cuando los valores ingresados están dentro del rango de los datos de entrenamiento.
""")