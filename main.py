# main.py
import os
from app import create_app

# Obtener el nombre de la configuración desde la variable de entorno FLASK_ENV
# Si no está definida, usa 'default' (que normalmente apunta a DevelopmentConfig)
config_name = os.getenv('FLASK_ENV', 'default')
app = create_app(config_name)

if __name__ == '__main__':
    # Ejecuta el servidor de desarrollo de Flask
    # host='0.0.0.0' permite conexiones desde otras máquinas en la red
    # debug=app.config['DEBUG'] usa el valor de la config cargada
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])