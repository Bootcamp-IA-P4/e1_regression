# 🌴 Sistema de Predicción de Precios Inmobiliarios de California 🏄‍♂️

<div align="center">
    <img src="https://img.shields.io/badge/California-Housing-ff9e7a?style=for-the-badge&logo=california&logoColor=white" alt="California Housing">
    <img src="https://img.shields.io/badge/Data-Prediction-4ECDC4?style=for-the-badge&logo=spark&logoColor=white" alt="Data Prediction">
</div>

> *"Construye tu casa en California, pero asegúrate de que tu modelo de predicción esté bien testeado..."* - Inspiración de Venice Beach, circa 2024

## 🎵 Bienvenido al Sistema Inteligente de Predicción de Precios 🎵

¡Descubre la aplicación más innovadora de predicción de precios de viviendas! Un proyecto que combina tecnología de vanguardia con el espíritu creativo de la era digital, transformando datos inmobiliarios en predicciones precisas y accesibles.

## 🌊 La Historia Detrás del Proyecto 🌊

Todo comenzó cuando un equipo de programadores apasionados encontró el dataset California Housing y decidió llevar la predicción de precios a otro nivel:

1. **Análisis de Datos Profundo** 🔍: Exploramos exhaustivamente el dataset California Housing, identificando patrones, correlaciones y insights ocultos. Documentamos cada paso en `eda/california-housing-eda.ipynb`.

2. **Transformación Inteligente** 🔄: Convertimos unidades del sistema imperial al métrico, tradujimos variables al español y generamos un dataset limpio `train_es_clean.csv`.

3. **Batalla de Algoritmos** 🥊: Entrenamos y evaluamos múltiples modelos de regresión:
   - Regresión Lineal: El método clásico
   - Regresión Ridge: El modelo equilibrado
   - Árboles de Decisión: El enfoque estructurado
   - Regresión Bayesiana: El método sofisticado

4. **Ridge: El Modelo Campeón** 👑: Tras rigurosas pruebas (documentadas en `ml-models/ridge-regression.ipynb`), nuestro modelo Ridge se destacó por su rendimiento, estabilidad y capacidad de manejo de multicolinealidad.

## 🎮 Características Innovadoras 🎮

* **Diseño Moderno** 💾: Interfaz intuitiva y visualmente atractiva
* **Modelo Ridge Optimizado** 📊: Predicción de precisión superior
* **Interfaz Paso a Paso** 🚶: Experiencia de usuario guiada y clara
* **Persistencia en MySQL** 📜: Almacenamiento de datos robusto y confiable
* **Flask + Docker** 💪: Infraestructura escalable y flexible
* **Tests Automatizados** 🧪: Verificación completa de funcionalidad

## 📊 Variables del Modelo Ridge 📊

Nuestro modelo utiliza un conjunto completo de variables para sus predicciones:

### Variables Numéricas:
- `CalidadGeneral`: Clasificación general de la vivienda (1-10)
- `MetrosHabitables`: Área habitable en metros cuadrados
- `CochesGaraje`: Capacidad del garaje
- `AreaGaraje`: Superficie del garaje
- `MetrosTotalesSotano`: Área total del sótano
- `Metros1raPlanta`: Superficie de la primera planta
- `BañosCompletos`: Número de baños completos
- `TotalHabitacionesSobreSuelo`: Número de habitaciones
- `AñoConstrucción`: Año de construcción
- `AñoRenovación`: Año de última renovación
- `AreaRevestimientoMampostería`: Superficie de revestimiento
- `Chimeneas`: Número de chimeneas
- `MetrosAcabadosSótano1`: Área habitable del sótano
- `FrenteLote`: Ancho frontal del terreno

### Variables Categóricas:
- `CalidadExterior`: Calidad de materiales exteriores
- `CalidadCocina`: Calidad de la cocina
- `CalidadSótano`: Altura y acabado del sótano
- `AcabadoGaraje`: Tipo de acabado interior
- `AireAcondicionadoCentral`: Presencia de A/C central
- `CalidadChimenea`: Calidad de la chimenea
- `Cimentación`: Tipo de cimentación
- `TipoGaraje`: Ubicación/tipo del garaje
- `TipoRevestimientoMampostería`: Material del revestimiento
- `CalidadCalefacción`: Calidad del sistema de calefacción
- `Vecindario`: Ubicación dentro de Ames, Iowa

## 🔧 Pila Tecnológica 🔧

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-black?style=flat-square&logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-8.x-orange?style=flat-square&logo=mysql)
![Pandas](https://img.shields.io/badge/Pandas-1.5+-blueviolet?style=flat-square&logo=pandas)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.2+-orange?style=flat-square&logo=scikit-learn)
![Docker](https://img.shields.io/badge/Docker-20.10+-blue?style=flat-square&logo=docker)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3)
![pytest](https://img.shields.io/badge/pytest-7.0+-green?style=flat-square&logo=pytest)

## 📁 Estructura del Proyecto 📁

```
e1_regression/
├── app/                          # Núcleo de la aplicación
│   ├── __init__.py               # Inicialización del proyecto
│   ├── routes.py                 # Definición de rutas
│   ├── model_loader.py           # Cargador del modelo de Machine Learning
│   ├── models/                   # Modelos ORM para interacción con base de datos
│   │   ├── property.py           # Manejo de propiedades inmobiliarias
│   │   └── prediction.py         # Gestión de predicciones de precios
│   ├── templates/                # Plantillas HTML
│   │   ├── base.html             # Template base
│   │   ├── index.html            # Página de inicio
│   │   └── predict.html          # Calculadora de precios
│   ├── static/                   # Recursos estáticos
│   │   ├── css/                  # Hojas de estilo
│   │   │   ├── index.css         # Estilos principales
│   │   │   └── california-style.css # Estilos específicos
│   │   ├── js/                   # Scripts JavaScript
│   │   │   ├── index.js          # Funcionalidad básica
│   │   │   └── california-form.js # Lógica del formulario
│   │   └── imgs/                 # Imágenes
├── database/                     # Scripts de base de datos
│   ├── schema.sql                # Estructura de tablas
│   └── seed.sql                  # Datos iniciales (opcional)
├── eda/                          # Análisis Exploratorio de Datos
│   └── california-housing-eda.ipynb # Exploración de datos
├── ml-models/                    # Laboratorio de modelos de Machine Learning
│   ├── export-models/            # Modelos entrenados
│   ├── lineal-regression.ipynb   # Exploración de regresión lineal
│   ├── ridge-regression.ipynb    # Desarrollo del modelo Ridge
│   ├── tree-decision.ipynb       # Experimentos con árboles de decisión
│   └── bayessian-regression.ipynb # Intentos con enfoque bayesiano
├── model/                        # Modelos en producción
│   └── modelo_ridge_california_housing.pkl # Modelo Ridge serializado
├── data/                         # Conjunto de datos
│   ├── train.csv                 # Dataset original
│   ├── train_es.csv              # Versión en español
│   └── train_es_clean.csv        # Versión limpia y métrica
├── tests/                        # Tests automatizados
│   ├── test_model_loader.py      # Verificación de carga de modelo
│   ├── test_prediction.py        # Verificación de predicciones
│   └── conftest.py               # Configuración compartida
├── main.py                       # Punto de entrada principal
├── config.py                     # Configuraciones de entornos
├── Dockerfile                    # Configuración para contenerización
├── compose.yaml                  # Orquestación de servicios Docker
└── README.md                     # Documentación del proyecto
```

## 🏄‍♂️ Instalación 🏄‍♂️

### Prerequisitos

* Python 3.8+
* MySQL 8+
* Docker & Docker Compose (opcional)
* pytest

### Instalación Manual

1. **Clonar el repositorio:**
   ```bash
   git clone <url-repo>
   cd e1_regression
   ```

2. **Crear entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar archivo .env:**
   ```
   FLASK_APP=main.py
   FLASK_ENV=development
   SECRET_KEY='tu_clave_secreta_super_segura'
   MYSQL_HOST='localhost'
   MYSQL_USER='tu_usuario'
   MYSQL_PASSWORD='tu_password_seguro'
   MYSQL_DB='housing_predictions'
   MYSQL_CURSORCLASS='DictCursor'
   MODEL_PATH='model/modelo_ridge_california_housing.pkl'
   ```

5. **Preparar base de datos:**
   ```bash
   mysql -u root -p < database/schema.sql
   ```

6. **Lanzar la aplicación:**
   ```bash
   flask run --port=5000
   ```

### Instalación Con Docker

Para una instalación rápida y sin complicaciones:

```bash
# Levantar todo el stack con un solo comando:
docker compose up -d

# Para ver los logs mientras corre:
docker compose logs -f
```

## 🧪 Testing: Verificación de Calidad 🧪

Nuestras pruebas automatizadas son compatibles con instalación local y Docker:

### Test Individual

```bash
# Verifica que el modelo carga correctamente:
pytest -xvs tests/test_model_loader.py

# Comprueba que las predicciones funcionan:
pytest -xvs tests/test_prediction.py
```

### Test Suite Completo

```bash
# Ejecuta todas las pruebas disponibles:
pytest -xvs tests/
```

## 🚀 Uso de la Aplicación 🚀

1. **Accede a la aplicación** a través de `http://localhost:5000`

2. **Navega a "Calcular Precio"**

3. **Sigue el proceso paso a paso** completando los campos:
   - Elige la calidad general (de 1 a 10)
   - Indica metros habitables, capacidad de garaje y otras características
   - Selecciona detalles como año de construcción, número de baños y habitaciones
   - Define acabados, materiales y ubicación

4. **Recibe tu predicción** generada por el modelo Ridge

## 👥 Equipo de Desarrollo 👥

* [**Veida Velázquez (Scrum Master)**](https://github.com/DarthVada36) - Liderazgo estratégico y gestión de proyecto
* [**Pepe Ruiz**](https://github.com/peperuizdev) - Desarrollo de frontend
* [**Omar Lengua**](https://github.com/Omarlsant) - Desarrollo de backend
* [**Maximiliano Scarlato**](https://github.com/MaximilianoScarlato) - Ingeniería de Machine Learning

## 📜 Licencia 📜

Proyecto bajo Licencia de Factoría F5: Aprender, Compartir y Citar la Fuente.

---

*"Predecir precios de viviendas con precisión: el futuro es ahora"*

*Creado con pasión por el Squad "Pacific Dreams" de Factoría F5* 🌊
