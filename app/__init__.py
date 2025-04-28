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

    # Inicializar extensiones
    try:
        mysql.init_app(app)
        app.logger.info("Extensión MySQL inicializada.")
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

    # (Opcional) Registrar manejadores de error globales
    # @app.errorhandler(404)
    # def not_found_error(error):
    #     return render_template('404.html'), 404
    #
    # @app.errorhandler(500)
    # def internal_error(error):
    #     # Podrías hacer rollback de la sesión de BD aquí si usas SQLAlchemy
    #     return render_template('500.html'), 500

    app.logger.info("Aplicación creada exitosamente.")
    return app