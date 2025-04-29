# 🏄‍♂️ CALIFORNIA DREAMIN' 🌴

![Banner](https://img.shields.io/badge/California-Dreamin'-ff9e7a?style=for-the-badge&logo=california&logoColor=white)

> *"Construye tu casa en California, pero asegúrate de que tu modelo de predicción esté bien testeado..."* - Proverbio de Venice Beach, circa 1995

## 🎵 Bienvenido al Sistema Radical de Predicción de Precios 🎵

¡Cowabunga! Has encontrado la aplicación más tubular de predicción de precios de viviendas ambientada en los mejores años 90. Época de Nirvana, Tamagotchis y sueños de tener una mansión en Malibú, cuando los precios inmobiliarios eran tan volátiles como los peinados de Boy Bands. ¡Totally awesome!

## 🌊 La Historia (As Told By MTV) 🌊

Todo comenzó cuando cuatro valientes programadores encontraron un dataset llamado California Housing y decidieron darle un giro noventero:

1. **El EDA Más Radical** 🔍: Exploramos profundamente el dataset California Housing, identificando outliers, correlaciones y patrones ocultos en los datos como detective de "Los Expedientes Secretos X". Documentamos todo el proceso en `eda/california-housing-eda.ipynb`.

2. **Traducción y Transformación** 🔄: Convertimos las unidades del sistema imperial al métrico (adiós pies cuadrados, hola metros cuadrados), tradujimos todas las variables al español y limpiamos los datos para obtener nuestro propio dataset `train_es_clean.csv`. ¡Hasta la vista, baby!

3. **Batalla de Algoritmos** 🥊: Entrenamos y evaluamos múltiples modelos de regresión:
   - Regresión Lineal: El clásico, como las Converse All-Star
   - Regresión Ridge: El equilibrado, como un monopatín bien ajustado
   - Árboles de Decisión: El estructurado, como un walkman bien organizado
   - Regresión Bayesiana: El sofisticado, como un discman con anti-skip

4. **Ridge: El Campeón Indiscutible** 👑: Después de rigurosas pruebas y comparaciones (documentadas en `ml-models/ridge-regression.ipynb`), nuestro modelo Ridge emergió como el ganador por su mejor rendimiento, estabilidad y capacidad para manejar multicolinealidad.

## 🎮 Features Más Cool Que un Game Boy Color 🎮

* **Diseño Inspirado en los 90s** 💾: Colores vibrantes, sombras audaces y patrones geométricos que harían sentir en casa a Zack Morris
* **Modelo Ridge Optimizado** 📊: Un modelo de predicción más preciso que las predicciones de Nostradamus en MTV
* **Interfaz Paso a Paso** 🚶: Una experiencia guiada más clara que las instrucciones de un VHS
* **Persistencia en MySQL** 📜: Almacenamiento de datos más confiable que tus cintas de casete favoritas
* **Flask + Docker** 💪: Una combinación más poderosa que los Mighty Morphin Power Rangers
* **Tests Automatizados** 🧪: Verificación de funcionalidad más completa que un chequeo de tu Tamagotchi

## 📊 Variables del Modelo Ridge 📊

Nuestro campeón, el modelo Ridge, utiliza estas variables para sus predicciones (como Capitán Planeta usa los poderes de su anillo):

### Variables Numéricas:
- `CalidadGeneral`: Clasificación general de la vivienda (1-10)
- `MetrosHabitables`: Área habitable en metros cuadrados
- `CochesGaraje`: Capacidad del garaje en número de coches
- `AreaGaraje`: Superficie del garaje en metros cuadrados
- `MetrosTotalesSotano`: Área total del sótano en metros cuadrados
- `Metros1raPlanta`: Superficie de la primera planta en metros cuadrados
- `BañosCompletos`: Número de baños completos
- `TotalHabitacionesSobreSuelo`: Número de habitaciones (sin contar sótano)
- `AñoConstrucción`: Año en que se construyó la vivienda
- `AñoRenovación`: Año de la última renovación
- `AreaRevestimientoMampostería`: Superficie de revestimiento en metros cuadrados
- `Chimeneas`: Número de chimeneas
- `MetrosAcabadosSótano1`: Área habitable del sótano en metros cuadrados
- `FrenteLote`: Ancho frontal del terreno en metros

### Variables Categóricas:
- `CalidadExterior`: Calidad de materiales exteriores (Ex, Gd, TA, Fa)
- `CalidadCocina`: Calidad de la cocina (Ex, Gd, TA, Fa)
- `CalidadSótano`: Altura y acabado del sótano (Ex, Gd, TA, Fa, NoSótano)
- `AcabadoGaraje`: Tipo de acabado interior del garaje (Fin, RFn, Unf, NoGaraje)
- `AireAcondicionadoCentral`: Presencia de A/C central (Y, N)
- `CalidadChimenea`: Calidad de la chimenea (Ex, Gd, TA, Fa, Po, NoTiene)
- `Cimentación`: Tipo de cimentación (PConc, CBlock, BrkTil, Wood, Slab, Stone)
- `TipoGaraje`: Ubicación/tipo del garaje (Attchd, Detchd, BuiltIn, CarPort, Basment, NoGaraje)
- `TipoRevestimientoMampostería`: Material del revestimiento (BrkFace, Stone, BrkCmn, Ninguno)
- `CalidadCalefacción`: Calidad y condición del sistema de calefacción (Ex, Gd, TA, Fa, Po)
- `Vecindario`: Ubicación dentro de Ames, Iowa (25 vecindarios distintos)

¡Con estas variables, nuestro modelo Ridge predice precios como Marty McFly viaja en el tiempo: con precisión y estilo!

## 🔧 Mix Tecnológico - Lado A 🔧

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-black?style=flat-square&logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-8.x-orange?style=flat-square&logo=mysql)
![Pandas](https://img.shields.io/badge/Pandas-1.5+-blueviolet?style=flat-square&logo=pandas)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.2+-orange?style=flat-square&logo=scikit-learn)
![Docker](https://img.shields.io/badge/Docker-20.10+-blue?style=flat-square&logo=docker)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3)
![pytest](https://img.shields.io/badge/pytest-7.0+-green?style=flat-square&logo=pytest)

## 📁 El Mapa del Tesoro - Estructura del Proyecto 📁

```
e1_regression/
├── app/                          # Núcleo de la aplicación, como MTV era el núcleo de la cultura pop
│   ├── __init__.py               # La introducción, como el intro de "Fresh Prince of Bel-Air"
│   ├── routes.py                 # Define las rutas, como un mapa de Highway 1
│   ├── model_loader.py           # Cargador del modelo ML, como quien carga un casete favorito
│   ├── models/                   # Modelos ORM para interacción con DB
│   │   ├── property.py           # Maneja propiedades inmobiliarias
│   │   └── prediction.py         # Gestiona predicciones de precios
│   ├── templates/                # Plantillas HTML, el esqueleto de nuestra visión
│   │   ├── base.html             # Template base, como el álbum base de tu colección
│   │   ├── index.html            # Página de inicio, tu portal al mundo retro
│   │   └── predict.html          # Calculadora de precios, la estrella del show
│   ├── static/                   # Recursos estáticos, como tu colección de vinilos
│   │   ├── css/                  # Estilos que te transportan a la época dorada
│   │   │   ├── index.css         # Estilos de la página principal y base
│   │   │   └── california-style.css # El estilo de la calculadora, puro 90s
│   │   ├── js/                   # JavaScript para interactividad, como los efectos especiales
│   │   │   ├── index.js          # Funcionalidad básica
│   │   │   └── california-form.js # Lógica del formulario paso a paso
│   │   └── imgs/                 # Imágenes decorativas con vibra noventera
├── database/                     # Scripts para la base de datos
│   ├── schema.sql                # Estructura de tablas, como planos de tu casa soñada
│   └── seed.sql                  # Datos iniciales (opcional)
├── eda/                          # Análisis Exploratorio de Datos
│   └── california-housing-eda.ipynb # Nuestro viaje a través de los datos
├── ml-models/                    # Laboratorio de modelos de ML
│   ├── export-models/            # Almacén de modelos entrenados
│   ├── lineal-regression.ipynb   # Exploración de regresión lineal
│   ├── ridge-regression.ipynb    # Desarrollo de nuestro modelo campeón
│   ├── tree-decision.ipynb       # Experimentos con árboles de decisión
│   └── bayessian-regression.ipynb # Intentos con enfoque bayesiano
├── model/                        # Modelos en producción
│   └── modelo_ridge_california_housing.pkl # Nuestro modelo estrella serializado
├── data/                         # Conjunto de datos
│   ├── train.csv                 # Dataset original de California Housing
│   ├── train_es.csv              # Versión traducida al español
│   └── train_es_clean.csv        # Versión limpia y metricada
├── tests/                        # Tests automatizados, porque somos profesionales
│   ├── test_model_loader.py      # Verifica la carga correcta del modelo
│   ├── test_prediction.py        # Asegura predicciones precisas
│   └── conftest.py               # Configuración compartida para tests
├── main.py                       # Punto de entrada principal, el piloto de esta nave
├── config.py                     # Configuraciones para diferentes entornos
├── Dockerfile                    # Receta para contenerizar la aplicación
├── compose.yaml                  # Orquestación de servicios Docker
└── README.md                     # La guía que estás leyendo ahora, ¡Totalmente rad!
```

## 🏄‍♂️ Instalación: Más Fácil Que Programar Tu VCR 🏄‍♂️

### Prerequisitos (Lo Básico Que Necesitas)

* Python 3.8+ (más versátil que un reloj Casio multifunción)
* MySQL 8+ (más robusto que una Game Boy después de caer en el agua)
* Docker & Docker Compose (opcional, pero más conveniente que un control remoto universal)
* pytest (para validar que todo está más en orden que tu colección de cromos)

### Instalación Manual (El Camino Clásico)

1. **Clona el repositorio como quien graba un mixtape personalizado:**
   ```bash
   git clone <url-repo>
   cd e1_regression
   ```

2. **Crea un entorno virtual más aislado que tu habitación de adolescente:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instala dependencias como quien completa un álbum de cromos:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura tu archivo .env con más secretos que tu agenda de estudiante:**
   ```
   FLASK_APP=main.py
   FLASK_ENV=development
   SECRET_KEY='tu_clave_secreta_super_radical'
   MYSQL_HOST='localhost'
   MYSQL_USER='tu_usuario'
   MYSQL_PASSWORD='tu_password_seguro'
   MYSQL_DB='housing_predictions'
   MYSQL_CURSORCLASS='DictCursor'
   MODEL_PATH='model/modelo_ridge_california_housing.pkl'
   ```

5. **Prepara la base de datos como preparabas tu estudio para grabar un casete:**
   ```bash
   mysql -u root -p < database/schema.sql
   ```

6. **Lanza la aplicación y viaja en el tiempo:**
   ```bash
   flask run --port=5000
   ```

### Instalación Con Docker (El Camino Express)

Para quienes prefieren la comodidad de los 90s tardíos, Docker es tan fácil como usar un CD en lugar de rebobinar casetes:

```bash
# Levanta todo el stack con un solo comando:
docker compose up -d

# Para ver los logs mientras corre:
docker compose logs -f
```

## 🧪 Testing: Certifica Tu Obra Maestra 🧪

Nuestras pruebas automatizadas son compatibles tanto con la instalación local como con Docker. Asegúrate de que todo funciona como un reloj con estos comandos:

### Test Individual (Precisión Quirúrgica)

```bash
# Verifica que el modelo carga correctamente:
pytest -xvs tests/test_model_loader.py

# Comprueba que las predicciones funcionan:
pytest -xvs tests/test_prediction.py
```

### Test Suite Completo (La Experiencia Total)

```bash
# Ejecuta todas las pruebas disponibles:
pytest -xvs tests/
```

Nuestros tests son compatibles con la instalación dockerizada, funcionando igual de bien que un Walkman dentro o fuera de su estuche protector.

## 🚀 Uso: Una Experiencia Más Fluida Que Tu Gel Para El Pelo 🚀

1. **Accede a la aplicación** a través de `http://localhost:5000` para ver el historial de predicciones, como quien revisa su colección de cromos.

2. **Navega a "Calcular Precio"** para iniciar tu aventura predictiva, como quien ponía su casete favorito.

3. **Sigue el proceso paso a paso** completando los campos sobre tu casa soñada:
   - Elige la calidad general (de 1 a 10)
   - Indica metros habitables, capacidad de garaje y otras características
   - Selecciona detalles como año de construcción, número de baños y habitaciones
   - Define acabados, materiales y ubicación

4. **Recibe tu predicción** generada por nuestro modelo Ridge y descubre si tu mansión soñada cuesta como un Lamborghini o como una colección completa de VHS.

## 👾 Squad Goals: El Dream Team 👾

* [**Veida Velázquez (Scrum Master)**](https://github.com/DarthVada36) - Gestiona el proyecto como Goku gestiona el Ki.
* [**Pepe Ruiz**](https://github.com/peperuizdev) - Desarrolla frontend como Bob Ross pinta árboles felices.
* [**Omar Lengua**](https://github.com/Omarlsant) - Maneja el backend como un DJ scratching vinilos.
* [**Maximiliano Scarlato**](https://github.com/MaximilianoScarlato) - Domina algoritmos y datos como Neo dominaba Matrix.

## 📜 Licencia: Las Reglas del Juego 📜

Este proyecto está bajo la Licencia de Factoría F5, que en buen cristiano significa: "Aprende, comparte y cita la fuente. ¡Keep it real!"

---

*"¿Y si te dijera que puede predecir el precio de tu casa? Whoa..."* – Keanu Reeves en "Matrix" de los 90s (quizás)

*Creado con más nostalgia que un maratón de "Salvados por la Campana" por el Squad "Pacific Dreams" de Factoría F5* 🤙
