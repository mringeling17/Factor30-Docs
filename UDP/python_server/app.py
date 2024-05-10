from flask import Flask, request, jsonify
import psycopg2
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()  # Add this line to load environment variables from .env file

app = Flask(__name__)
CORS(app)  # Esto habilitará CORS para todas las rutas y todas las orígenes

# Establecer conexión con la base de datos
def get_db_connection():
    conn = psycopg2.connect(
        host='db',
        database=os.environ['POSTGRES_DB'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'])
    return conn

@app.route('/receive_data', methods=['POST'])
def handle_data():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    print('recieved Data at ', datetime.now())
    
    cur.execute('INSERT INTO measurements (temperature, humidity, wind_speed, risk_level, uuid, received_at) VALUES (%s, %s, %s, %s, %s, %s)',
                (data['temperature'], data['humidity'], data['wind_speed'], data['risk_level'], data['uuid'], datetime.now()))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Data received"}), 201


@app.route('/recent_measurements')
def recent_measurements():
    conn = get_db_connection()
    cursor = conn.cursor()
    time_threshold = datetime.now() - timedelta(hours=10)
    # Prepara y ejecuta la consulta SQL
    cursor.execute("""
        SELECT * FROM measurements
        WHERE received_at >= %s
        ORDER BY received_at DESC;
    """, (time_threshold,))
    # Obtiene los resultados de la consulta
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    # Prepara los datos para la respuesta
    results = []
    for record in records:
        results.append({
            "id": record[0],
            "temperature": record[1],
            "humidity": record[2],
            "wind_speed": record[3],
            "risk_level": record[4],
            "uuid": record[5],
            "received_at": record[6].isoformat()  # Formatea datetime para JSON
        })
    return jsonify(results)  # Devuelve los datos en formato JSON


@app.route("/")
def index():
    return "Hello!!!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
