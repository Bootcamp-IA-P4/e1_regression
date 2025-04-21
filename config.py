import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """Clase base de configuración."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una-clave-secreta-por-defecto-insegura'
    MYSQL_HOST = os.environ.get('MYSQL_HOST')
    MYSQL_USER = os.environ.get('MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_DB = os.environ.get('MYSQL_DB')
    MYSQL_CURSORCLASS = os.environ.get('MYSQL_CURSORCLASS', 'DictCursor') # Usar DictCursor por defecto
    MODEL_PATH = os.environ.get('MODEL_PATH') or 'model/housing_model.joblib' # Ruta por defecto

class DevelopmentConfig(Config):
    """Configuración para desarrollo."""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Configuración para producción."""
    DEBUG = False
    FLASK_ENV = 'production'
    # Podrías añadir configuraciones específicas de producción aquí (logging, etc.)

# Diccionario para acceder a las configuraciones por nombre
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}