# app/__init__.py
import os
from flask import Flask
from flask_mysqldb import MySQL
from config import config_by_name
import logging # Importar logging

# Instancia de la extensión MySQL (sin inicializar app aún)
mysql = MySQL()

def create_app(config_name=None):
    """Fábrica de la aplicación Flask."""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')

    app = Flask(__name__)
    # Cargar configuración desde el objeto (config.py)
    app.config.from_object(config_by_name[config_name])

    # Configurar Logging Básico
    logging.basicConfig(level=getattr(logging, app.config.get('LOG_LEVEL', 'INFO')),
                        format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')

    app.logger.info(f"Iniciando aplicación con configuración: {config_name}")
    app.logger.debug(f"Configuración cargada: {app.config}")

    # Inicializar extensiones
    try:
        mysql.init_app(app)
        app.logger.info("Extensión MySQL inicializada.")
        
        # NUEVO CÓDIGO PARA CREAR LAS TABLAS
        def init_db():
            """Inicializa la base de datos si no existe"""
            cursor = None  # Inicializar antes para evitar UnboundLocalError
            
            # Usar contexto de aplicación
            with app.app_context():
                try:
                    cursor = mysql.connection.cursor()
                    
                    # Crear base de datos si no existe
                    cursor.execute("CREATE DATABASE IF NOT EXISTS housing_predictions")
                    cursor.execute("USE housing_predictions")
                    
                    # Crear tablas principales
                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS properties (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        calidad_general INT NOT NULL,
                        metros_habitables FLOAT NOT NULL,
                        coches_garaje INT NOT NULL,
                        area_garaje FLOAT NOT NULL,
                        metros_totales_sotano FLOAT NOT NULL,
                        metros_1ra_planta FLOAT NOT NULL,
                        banos_completos INT NOT NULL,
                        total_habitaciones_sobre_suelo INT NOT NULL,
                        ano_construccion INT NOT NULL,
                        ano_renovacion INT NOT NULL,
                        area_revestimiento_mamposteria FLOAT NOT NULL,
                        chimeneas INT NOT NULL,
                        metros_acabados_sotano_1 FLOAT NOT NULL,
                        frente_lote FLOAT NOT NULL,
                        calidad_exterior VARCHAR(10) NOT NULL,
                        calidad_cocina VARCHAR(10) NOT NULL,
                        calidad_sotano VARCHAR(10) NOT NULL,
                        acabado_garaje VARCHAR(10) NOT NULL,
                        aire_acondicionado_central VARCHAR(2) NOT NULL,
                        calidad_chimenea VARCHAR(10) NOT NULL,
                        cimentacion VARCHAR(10) NOT NULL,
                        tipo_garaje VARCHAR(10) NOT NULL,
                        tipo_revestimiento_mamposteria VARCHAR(10) NOT NULL,
                        calidad_calefaccion VARCHAR(10) NOT NULL,
                        vecindario VARCHAR(20) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                    """)
                    
                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS predictions (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        property_id INT NOT NULL,
                        predicted_value FLOAT NOT NULL,
                        actual_value FLOAT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
                    )
                    """)
                    
                    mysql.connection.commit()
                    app.logger.info("Base de datos inicializada correctamente")
                    
                except Exception as e:
                    app.logger.error(f"Error al inicializar la base de datos: {e}")
                    
                finally:
                    if cursor:
                        cursor.close()

        # Llamar a la función para crear las tablas
        init_db()
        
    except Exception as e:
        app.logger.error(f"Error al inicializar MySQL: {e}", exc_info=True)
        raise # Es crítico si la BD no funciona

    # Cargar el modelo de ML al inicio
    from . import model_loader # Importar el módulo
    try:
        with app.app_context(): # Asegura el contexto de la aplicación para el loader
             model_loader.load_model_on_startup(app)
    except (FileNotFoundError, ValueError, RuntimeError, Exception) as e:
         # El error ya se loggeó en el loader, solo informamos aquí
         app.logger.critical(f"La carga del modelo falló. La funcionalidad de predicción estará inactiva. Error: {e}")
         # Decide si la app debe detenerse. Por ahora, continúa pero sin modelo.

    # Registrar Blueprints
    from .routes import main_bp # Importación DENTRO de la función si hay dependencias circulares
    app.register_blueprint(main_bp) # SIN prefijo url_prefix si quieres que '/' funcione
    # Si pones app.register_blueprint(main_bp, url_prefix='/'), está bien también.
    app.logger.info("Blueprint 'main' registrado.")
    app.logger.info("Aplicación creada exitosamente.")
    return app