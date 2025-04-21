# API de Predicción de Precios de Vivienda con Flask  predicting-housing-api

✨ Un API web construida con Flask para predecir el valor medio de las viviendas utilizando un modelo de Machine Learning preentrenado, almacenando los datos y resultados en una base de datos MySQL. ✨

## 🚀 Descripción General

Este proyecto implementa una API RESTful y una interfaz web simple utilizando el microframework Flask. Permite a los usuarios ingresar características de una zona residencial (basadas en el dataset California Housing) y obtener una predicción del valor medio de la vivienda en esa área, generada por un modelo de regresión previamente entrenado.

La aplicación guarda cada conjunto de características ingresadas (como una 'propiedad') y su predicción correspondiente en una base de datos MySQL para su posterior análisis o visualización.

## 📋 Características Principales

*   **Interfaz Web Simple:**
    *   Página de inicio (`/`) que muestra predicciones recientes.
    *   Formulario (`/predict`) para ingresar datos y obtener una predicción instantánea.
*   **API RESTful:**
    *   Endpoint (`POST /api/v1/predictions`) para realizar predicciones programáticamente enviando datos JSON.
*   **Modelo de ML:** Carga un modelo de regresión preentrenado (formato `.pkl`) para realizar las predicciones.
*   **Persistencia en Base de Datos:** Almacena las características de entrada (`properties`) y los resultados de la predicción (`predictions`) en una base de datos MySQL.
*   **Estructura Organizada:** Sigue un patrón de diseño modular con Blueprints, modelos de datos, utilidades y configuración separada.
*   **Configuración Flexible:** Utiliza variables de entorno (`.env`) para gestionar la configuración sensible (claves secretas, credenciales de BD, ruta del modelo).
*   **Estilo Personalizado:** Incluye un archivo CSS básico para una presentación limpia.

## ⚙️ Tecnologías Utilizadas

*   **Backend:** Python 3.x
*   **Framework Web:** Flask
*   **Base de Datos:** MySQL
*   **Conector BD:** Flask-MySQLdb (basado en `mysqlclient` o compatible)
*   **Manipulación de Datos (Predicción):** Pandas
*   **Carga de Modelo:** Pickle (o Joblib si cambias el loader)
*   **Gestión de Entorno:** `venv`, `python-dotenv`
*   **Frontend:** HTML5, CSS3, Jinja2 (motor de plantillas de Flask)
*   **Servidor de Desarrollo:** Werkzeug (integrado con Flask)

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-black?style=flat-square&logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-8.x-orange?style=flat-square&logo=mysql)
![Pandas](https://img.shields.io/badge/Pandas-LATEST-blueviolet?style=flat-square&logo=pandas)
![HTML5](https://img.shields.io/badge/HTML5-orange?style=flat-square&logo=html5)
![CSS3](https://img.shields.io/badge/CSS3-blue?style=flat-square&logo=css3)

## 📁 Estructura del Proyecto

e1_regression/
├── main.py # Punto de entrada de la aplicación
├── config.py # Clases de configuración (lee .env)
├── .env # Archivo de variables de entorno
├── requirements.txt # Dependencias de Python
├── app/ # Directorio principal de la aplicación Flask
│ ├── init.py # Fábrica de la aplicación (create_app)
│ ├── routes.py # Definición de rutas (Blueprint)
│ ├── model_loader.py # Lógica para cargar el modelo ML
│ ├── models/ # Modelos de datos (interacción con BD)
│ │ ├── init.py
│ │ ├── property.py # Modelo para la tabla 'properties'
│ │ └── prediction.py # Modelo para la tabla 'predictions'
│ ├── utils/ # Funciones de utilidad
│ │ ├── init.py
│ │ └── db_utils.py # Utilidades para interactuar con la BD
│ ├── connection/ # (Opcional, podría contener lógica de conexión)
│ │ ├── init.py
│ │ └── db_connection.py
│ ├── templates/ # Plantillas HTML (Jinja2)
│ │ ├── base.html # Plantilla base
│ │ ├── index.html # Página principal
│ │ └── predict.html # Página de predicción (formulario y resultado)
│ └── static/ # Archivos estáticos (CSS, JS, Imágenes)
│ ├── css/
│ │ └── index.css # Hoja de estilos principal
│ ├── js/
│ │ └── index.js # (Placeholder para JS futuro)
│ └── imgs/
│ └── ... # (Placeholder para imágenes futuras)
├── database/ # Scripts SQL para la base de datos
│ ├── schema.sql # Script para crear la estructura de la BD y tablas
│ └── seed.sql # (Opcional) Script para datos iniciales
├── model/ # Carpeta para el modelo ML serializado
│ └── optimised_bayesian_pipeline.pkl # Modelo ML 
└── venv/ # Entorno virtual de Python


## 🔧 Instalación y Configuración

Sigue estos pasos para poner en marcha la aplicación localmente:

1.  **Clonar el Repositorio:**
    ```bash
    git clone <url-de-tu-repositorio>
    cd e1_regression
    ```

2.  **Crear y Activar Entorno Virtual:**
    ```bash
    # Linux / macOS
    python3 -m venv venv
    source venv/bin/activate

    # Windows (cmd / PowerShell)
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instalar Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Asegúrate de tener las cabeceras de desarrollo de MySQL/MariaDB si `mysqlclient` da problemas: `sudo apt-get install default-libmysqlclient-dev` en Debian/Ubuntu)*

4.  **Configurar Variables de Entorno:**
    *   Crea un archivo llamado `.env` en la raíz del proyecto (`e1_regression/`).
    *   Copia el contenido de `.env.example` (si lo creas) o añade las siguientes variables, **ajustando los valores a tu entorno**:

    ```dotenv
    # Flask Config
    FLASK_APP=main.py
    FLASK_ENV=development # Cambiar a 'production' en despliegue
    SECRET_KEY='tu_clave_secreta_muy_segura_y_aleatoria_aqui!' # ¡Genera una segura!

    # Database Config (Ajusta a tus credenciales de MySQL)
    MYSQL_HOST='localhost'
    MYSQL_USER='root'  # O tu usuario específico como 'db_bayessian'
    MYSQL_PASSWORD='tu_contraseña_mysql' # ¡Tu contraseña real!
    MYSQL_DB='housing_predictions'
    MYSQL_CURSORCLASS='DictCursor' # Recomendado

    # Model Config (Ajusta si el nombre/ruta cambia)
    MODEL_PATH='model/optimised_bayesian_pipeline.pkl'
    ```
    *   **¡Importante!** No subas tu archivo `.env` a Git. Asegúrate de que `.gitignore` lo incluya.

5.  **Base de Datos MySQL:**
    *   Asegúrate de tener un servidor MySQL instalado y ejecutándose.
    *   Conéctate a tu servidor MySQL (p.ej., con `mysql -u root -p`).
    *   **Crea la base de datos:**
        ```sql
        CREATE DATABASE IF NOT EXISTS housing_predictions CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        ```
    *   **(Opcional)** Si no usas `root`, crea un usuario específico y otórgale permisos (reemplaza `'tu_usuario'` y `'tu_contraseña'`):
        ```sql
        -- CREATE USER IF NOT EXISTS 'tu_usuario'@'localhost' IDENTIFIED BY 'tu_contraseña';
        -- GRANT ALL PRIVILEGES ON housing_predictions.* TO 'tu_usuario'@'localhost';
        -- FLUSH PRIVILEGES;
        ```
    *   **Ejecuta el Schema:** Sal de la consola MySQL y ejecuta desde la terminal (en la raíz del proyecto):
        ```bash
        mysql -u TU_USUARIO_MYSQL -p housing_predictions < database/schema.sql
        ```
        (Reemplaza `TU_USUARIO_MYSQL` por `root` o tu usuario específico. Te pedirá la contraseña).

6.  **Colocar el Modelo:**
    *   Asegúrate de que tu archivo de modelo preentrenado (`optimised_bayesian_pipeline.pkl`) se encuentra **dentro** de la carpeta `model/` en la raíz del proyecto.

## ▶️ Ejecutar la Aplicación

Una vez completada la instalación y configuración:

1.  Asegúrate de que tu entorno virtual esté activado.
2.  Ejecuta el script principal:
    ```bash
    python main.py
    ```
    o usando el comando de Flask:
    ```bash
    flask run --host=0.0.0.0 --port=5000
    ```

3.  La aplicación estará disponible en: `http://127.0.0.1:5000` (o la IP de tu máquina en el puerto 5000).

## 💻 Uso

### Interfaz Web

*   **Página Principal (`/`):** Accede a `http://127.0.0.1:5000/`. Verás una introducción y una tabla (inicialmente vacía) con las últimas predicciones guardadas.
*   **Formulario de Predicción (`/predict`):** Accede a `http://127.0.0.1:5000/predict`. Rellena los campos del formulario con los datos de la zona y haz clic en "Predecir Valor". Se mostrará el resultado y los datos se guardarán en la base de datos.

### API Endpoint

*   **Endpoint:** `POST /api/v1/predictions`
*   **Método:** `POST`
*   **Headers:** `Content-Type: application/json`
*   **Cuerpo (Body):** Un objeto JSON con las características requeridas. Los nombres de las claves deben coincidir con los esperados en `routes.py` (ej. `MedInc`, `HouseAge`, etc.).

    **Ejemplo de Petición JSON:**
    ```json
    {
        "MedInc": 8.3,
        "HouseAge": 40,
        "AveRooms": 6.5,
        "AveBedrms": 1.1,
        "Population": 400,
        "AveOccup": 2.8,
        "Latitude": 37.8,
        "Longitude": -122.2,
        "ActualValue": 4.5  // Opcional: Para guardar valor real si se conoce
    }
    ```

*   **Respuesta Exitosa (Código `201 Created`):**
    ```json
    {
        "message": "Predicción creada exitosamente.",
        "property": {
            "id": 1, // ID de la propiedad creada
            "med_income": 8.3,
            "house_age": 40.0,
            "ave_rooms": 6.5,
            "ave_bedrooms": 1.1,
            "population": 400.0,
            "ave_occupancy": 2.8,
            "latitude": 37.8,
            "longitude": -122.2,
            "median_value": 4.5, // Valor real guardado (si se envió)
            "created_at": "..." // Fecha/hora de creación
        },
        "prediction": {
            "id": 1, // ID de la predicción creada
            "property_id": 1,
            "predicted_value": 4.853, // Valor predicho por el modelo
            "actual_value": 4.5, // Valor real guardado (si se envió)
            "created_at": "..." // Fecha/hora de creación
        }
    }
    ```

*   **Respuestas de Error:**
    *   `400 Bad Request`: Datos JSON inválidos, faltan campos requeridos o tipos de datos incorrectos.
    *   `415 Unsupported Media Type`: Si no se envía `Content-Type: application/json`.
    *   `500 Internal Server Error`: Si ocurre un error inesperado en el servidor (ej. modelo no cargado, error de BD irrecuperable).

## 💡 Modelo de Machine Learning

*   El modelo (`optimised_bayesian_pipeline.pkl`) es cargado al inicio de la aplicación.
*   Se espera que sea un objeto serializado (usando `pickle`) compatible con la interfaz de Scikit-Learn (es decir, que tenga un método `.predict()`).
*   El modelo debe esperar un DataFrame de Pandas como entrada para `.predict()`, con columnas que coincidan con las claves del formulario/API: `['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population', 'AveOccup', 'Latitude', 'Longitude']`.

## ☁️ Despliegue (Notas)

*   Para producción, **NO USES** el servidor de desarrollo de Flask (`flask run` o `python main.py`).
*   Cambia `FLASK_ENV` a `production` en tu configuración (`.env` o variables de entorno del servidor).
*   Utiliza un servidor WSGI robusto como Gunicorn o Waitress detrás de un servidor proxy inverso como Nginx o Apache.
*   Asegúrate de que la configuración de la base de datos y la `SECRET_KEY` sean seguras en el entorno de producción.

## 🙏 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir cambios mayores o simplemente envía un Pull Request para correcciones menores.

## 📄 Licencia

Este proyecto está bajo la Licencia Factoría F5, al ser un proyecto colaborativo.

---