import os
import sqlite3
import pickle
from flask import Flask, render_template, request, g, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Configuración de rutas
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'model', 'modelo_ridge_california_housing.pkl')
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'predictions.db')

# Cargar modelo
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

# Conexión a la base de datos
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Crear tabla si no existe
def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prediction_created_at TEXT,
                MedInc REAL,
                HouseAge REAL,
                AveRooms REAL,
                AveBedrms REAL,
                Population REAL,
                AveOccup REAL,
                Latitude REAL,
                Longitude REAL,
                predicted_value REAL
            )
        ''')
        db.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        try:
            features = [
                float(request.form['MedInc']),
                float(request.form['HouseAge']),
                float(request.form['AveRooms']),
                float(request.form['AveBedrms']),
                float(request.form['Population']),
                float(request.form['AveOccup']),
                float(request.form['Latitude']),
                float(request.form['Longitude'])
            ]
            pred = model.predict([features])
            prediction = round(pred[0], 2)
            # Guardar en la base de datos
            db = get_db()
            db.execute('''
                INSERT INTO predictions (
                    prediction_created_at, MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude, predicted_value
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                features[0], features[1], features[2], features[3],
                features[4], features[5], features[6], features[7],
                prediction
            ))
            db.commit()
        except Exception as e:
            prediction = f"Error en la predicción: {e}"

    # Obtener últimas 10 predicciones
    db = get_db()
    cur = db.execute('SELECT * FROM predictions ORDER BY id DESC LIMIT 10')
    recent_predictions = cur.fetchall()
    return render_template('index.html', prediction=prediction, recent_predictions=recent_predictions)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

