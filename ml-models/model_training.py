import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import pickle
import os

# Configuración para visualizaciones
plt.style.use('seaborn-v0_8-whitegrid')
sns.set(font_scale=1.2)

# Creamos directorio para guardar resultados
os.makedirs('resultados', exist_ok=True)

# 1. Cargar los datos
print("Cargando datos...")
data = pd.read_csv('../data/train_es_clean.csv')
print(f"Datos cargados: {data.shape[0]} filas y {data.shape[1]} columnas")

# 2. Separar variables predictoras (X) y variable objetivo (y)
y = data['PrecioVenta']

# 3. Crear múltiples modelos con diferente número de variables
print("\n=== Modelo 1: Solo CalidadGeneral ===")
X_single = data[['CalidadGeneral']]
X_train_1, X_test_1, y_train_1, y_test_1 = train_test_split(
    X_single, y, test_size=0.2, random_state=42)

# Normalización de características (opcional para una sola variable, pero recomendado)
scaler = StandardScaler()
X_train_1_scaled = scaler.fit_transform(X_train_1)
X_test_1_scaled = scaler.transform(X_test_1)

# Entrenar el modelo 1
model_1 = LinearRegression()
model_1.fit(X_train_1_scaled, y_train_1)

# Evaluar modelo 1
y_pred_train_1 = model_1.predict(X_train_1_scaled)
y_pred_test_1 = model_1.predict(X_test_1_scaled)

train_r2_1 = r2_score(y_train_1, y_pred_train_1)
test_r2_1 = r2_score(y_test_1, y_pred_test_1)
train_rmse_1 = np.sqrt(mean_squared_error(y_train_1, y_pred_train_1))
test_rmse_1 = np.sqrt(mean_squared_error(y_test_1, y_pred_test_1))

print(f"R² en entrenamiento: {train_r2_1:.4f}")
print(f"R² en prueba: {test_r2_1:.4f}")
print(f"RMSE en entrenamiento: {train_rmse_1:.2f}")
print(f"RMSE en prueba: {test_rmse_1:.2f}")
print(f"Diferencia de R²: {train_r2_1 - test_r2_1:.4f}")
print(f"Diferencia porcentual en RMSE: {abs((train_rmse_1 - test_rmse_1) / train_rmse_1 * 100):.2f}%")

# Visualizar modelo 1 (relación entre calidad y precio)
plt.figure(figsize=(10, 6))
plt.scatter(X_test_1, y_test_1, alpha=0.5, label='Datos reales')
plt.plot(X_test_1, y_pred_test_1, color='red', linewidth=2, label='Predicción')
plt.xlabel('Calidad General')
plt.ylabel('Precio de Venta ($)')
plt.title('Modelo 1: Precio vs Calidad General')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('resultados/modelo_simple_calidad.png')
plt.close()

# Modelo 2: Usar las 5 variables numéricas más importantes
print("\n=== Modelo 2: Top 5 variables numéricas ===")
X_top5 = data[['CalidadGeneral', 'MetrosHabitables', 'CochesGaraje', 
               'ÁreaGaraje', 'MetrosTotalesSótano']]
X_train_2, X_test_2, y_train_2, y_test_2 = train_test_split(
    X_top5, y, test_size=0.2, random_state=42)

# Normalización
scaler_2 = StandardScaler()
X_train_2_scaled = scaler_2.fit_transform(X_train_2)
X_test_2_scaled = scaler_2.transform(X_test_2)

# Entrenar el modelo 2: Regresión Lineal
model_2 = LinearRegression()
model_2.fit(X_train_2_scaled, y_train_2)

# Evaluar modelo 2
y_pred_train_2 = model_2.predict(X_train_2_scaled)
y_pred_test_2 = model_2.predict(X_test_2_scaled)

train_r2_2 = r2_score(y_train_2, y_pred_train_2)
test_r2_2 = r2_score(y_test_2, y_pred_test_2)
train_rmse_2 = np.sqrt(mean_squared_error(y_train_2, y_pred_train_2))
test_rmse_2 = np.sqrt(mean_squared_error(y_test_2, y_pred_test_2))

print(f"R² en entrenamiento: {train_r2_2:.4f}")
print(f"R² en prueba: {test_r2_2:.4f}")
print(f"RMSE en entrenamiento: {train_rmse_2:.2f}")
print(f"RMSE en prueba: {test_rmse_2:.2f}")
print(f"Diferencia de R²: {train_r2_2 - test_r2_2:.4f}")
print(f"Diferencia porcentual en RMSE: {abs((train_rmse_2 - test_rmse_2) / train_rmse_2 * 100):.2f}%")

# Modelo 3: Top 5 variables con Ridge (regularización)
print("\n=== Modelo 3: Top 5 variables con Ridge ===")
model_3 = Ridge(alpha=1.0)  # Alpha es el parámetro de regularización
model_3.fit(X_train_2_scaled, y_train_2)

# Evaluar modelo 3
y_pred_train_3 = model_3.predict(X_train_2_scaled)
y_pred_test_3 = model_3.predict(X_test_2_scaled)

train_r2_3 = r2_score(y_train_2, y_pred_train_3)
test_r2_3 = r2_score(y_test_2, y_pred_test_3)
train_rmse_3 = np.sqrt(mean_squared_error(y_train_2, y_pred_train_3))
test_rmse_3 = np.sqrt(mean_squared_error(y_test_2, y_pred_test_3))

print(f"R² en entrenamiento: {train_r2_3:.4f}")
print(f"R² en prueba: {test_r2_3:.4f}")
print(f"RMSE en entrenamiento: {train_rmse_3:.2f}")
print(f"RMSE en prueba: {test_rmse_3:.2f}")
print(f"Diferencia de R²: {train_r2_3 - test_r2_3:.4f}")
print(f"Diferencia porcentual en RMSE: {abs((train_rmse_3 - test_rmse_3) / train_rmse_3 * 100):.2f}%")

# Comparación de modelos
print("\n=== Comparación de modelos ===")
models_comparison = pd.DataFrame({
    'Modelo': ['Modelo 1: Solo Calidad', 'Modelo 2: Top 5 variables', 'Modelo 3: Ridge con Top 5'],
    'R² Entrenamiento': [train_r2_1, train_r2_2, train_r2_3],
    'R² Prueba': [test_r2_1, test_r2_2, test_r2_3],
    'RMSE Entrenamiento': [train_rmse_1, train_rmse_2, train_rmse_3],
    'RMSE Prueba': [test_rmse_1, test_rmse_2, test_rmse_3],
    'Diferencia R²': [train_r2_1 - test_r2_1, train_r2_2 - test_r2_2, train_r2_3 - test_r2_3],
    'Diferencia % RMSE': [abs((train_rmse_1 - test_rmse_1) / train_rmse_1 * 100), 
                         abs((train_rmse_2 - test_rmse_2) / train_rmse_2 * 100),
                         abs((train_rmse_3 - test_rmse_3) / train_rmse_3 * 100)]
})
print(models_comparison)

# Guardar el mejor modelo (usaremos el modelo 3 que probablemente tenga mejor balance)
with open('resultados/modelo_ridge.pkl', 'wb') as f:
    pickle.dump({'model': model_3, 'scaler': scaler_2, 'features': X_top5.columns.tolist()}, f)
print("\nModelo Ridge guardado en 'resultados/modelo_ridge.pkl'")

# Visualizar predicciones vs. reales para el modelo 3
plt.figure(figsize=(10, 6))
plt.scatter(y_test_2, y_pred_test_3, alpha=0.5)
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')
plt.xlabel('Precio Real')
plt.ylabel('Precio Predicho')
plt.title('Predicciones vs Valores Reales (Modelo Ridge)')
plt.grid(True, alpha=0.3)
plt.savefig('resultados/predicciones_ridge.png')
plt.close()

# Importancia de características para el modelo Ridge
feature_importance = pd.DataFrame({
    'Característica': X_top5.columns,
    'Coeficiente': model_3.coef_
})
feature_importance['Importancia Absoluta'] = abs(feature_importance['Coeficiente'])
feature_importance = feature_importance.sort_values('Importancia Absoluta', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x='Importancia Absoluta', y='Característica', data=feature_importance)
plt.title('Importancia de Características (Ridge)')
plt.tight_layout()
plt.savefig('resultados/importancia_caracteristicas_ridge.png')
plt.close()

print("\n✅ Entrenamiento y evaluación de modelos simplificados completados!")