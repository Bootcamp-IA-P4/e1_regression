from flask import Flask
from config import Config
from app.database import init_app as init_db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializar la conexión a la base de datos
    init_db(app)
    
    # Registrar las rutas
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app