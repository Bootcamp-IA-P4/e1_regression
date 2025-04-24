from flask import Flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)

# Configuración de MySQL usando variables de entorno
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT'))
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

# Crear la instancia de MySQL
mysql = MySQL(app)

@app.route('/')
def index():
    return "Bienvenido. Visita /test_db para probar la conexión a la base de datos."

@app.route('/test_db')
def test_db():
    cur = mysql.connection.cursor()
    cur.execute('SELECT DATABASE()')
    db = cur.fetchone()
    return f"Conectado a la base de datos: {db[0]}"

if __name__ == "__main__":
    app.run(debug=True)