# Proyecto de Predicción de Precios de Casas

Este proyecto implementa un modelo de regresión lineal para predecir precios de casas basado en características como tamaño, calidad, ubicación y más.

## Estructura del Proyecto

├── data/
│ └── train_es_clean.csv # Datos limpios de casas 
├── eda/ 
│ └── california-housing-eda.ipynb # Análisis exploratorio de datos 
├── resultados/ # Directorio generado con resultados y visualizaciones 
├── model_training.py # Script para entrenar y evaluar el modelo 
├── feature_importance.py # Análisis de importancia de características 
├── app.py # Aplicación Streamlit para uso del modelo 
├── informe_modelo.md # Informe detallado del rendimiento 
└── README.md # Este archivo

## Requisitos

Para ejecutar este proyecto se necesitan las siguientes dependencias:

```bash
pip install -r requirements.txt
```

## Uso

1. Entrenar el modelo:

```bash
python model_training.py
```

2. Analizar importancia de características:

```bash
python feature_importance.py
```

3. Analizar importancia de características:

```bash
streamlit run app.py
```