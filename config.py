import os
from dotenv import load_dotenv

# Cargar variables desde archivo .env
load_dotenv()

class Config:
    # Configuración general
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-por-defecto'
    
    # Configuración MySQL
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or ''
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'housing_predictions'
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT') or 3306)
    
    # Otras configuraciones
    DEBUG = os.environ.get('FLASK_DEBUG') == 'True' or True
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'app', 'static', 'uploads')