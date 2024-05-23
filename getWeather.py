import requests
import psycopg2
import datetime
from time import sleep

# Configuración de la API y la base de datos
BASE_URL = 'https://archive-api.open-meteo.com/v1/archive'
DB_HOST = 'aws-0-eu-central-1.pooler.supabase.com'
DB_NAME = 'postgres'
DB_USER = 'postgres.karyjqxvursphmmomvky'
DB_PASSWORD = 'i1mQWy0EzJHz27Pd'
DB_PORT = '5432'  # Asegúrate de que este sea el puerto correcto

# Conectar a la base de datos
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    print("Conexión exitosa a la base de datos")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
    exit()

cursor = conn.cursor()

def get_weather_data(lat, lon, start_date, end_date):
    params = {
        'latitude': lat,
        'longitude': lon,
        'start_date': start_date,
        'end_date': end_date,
        'hourly': ['temperature_2m', 'relative_humidity_2m', 'wind_speed_10m']
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        print(f"Error en la solicitud: {response.json()}")
    return response.json()

def save_weather_data(data):
    hourly_data = data.get('hourly', {})
    timestamps = hourly_data.get('time', [])
    temperatures = hourly_data.get('temperature_2m', [])
    humidities = hourly_data.get('relative_humidity_2m', [])
    wind_speeds = hourly_data.get('wind_speed_10m', [])

    for i, timestamp in enumerate(timestamps):
        cursor.execute("""
            INSERT INTO weather_data (date_time, temperature, humidity, windspeed, weather_description)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (date_time) DO NOTHING
        """, (
            timestamp,
            temperatures[i] if i < len(temperatures) else None,
            humidities[i] if i < len(humidities) else None,
            wind_speeds[i] if i < len(wind_speeds) else None,
            None  # Open-Meteo no proporciona descripciones del clima
        ))
    conn.commit()

def fetch_data(lat, lon):
    start_date = datetime.datetime.now() - datetime.timedelta(days=10*365)
    end_date = datetime.datetime.now()

    current_date = start_date
    api_calls = 0
    days_per_request = 90  # 3 meses

    while current_date < end_date:
        next_date = current_date + datetime.timedelta(days=days_per_request)
        if next_date > end_date:
            next_date = end_date

        cursor.execute("SELECT 1 FROM weather_data WHERE date_time BETWEEN %s AND %s", (current_date, next_date))
        if True:
            print(f"Fetching data for {current_date.strftime('%Y-%m-%d')} to {next_date.strftime('%Y-%m-%d')}")
            weather_data = get_weather_data(lat, lon, current_date.strftime('%Y-%m-%d'), next_date.strftime('%Y-%m-%d'))
            if 'hourly' in weather_data:
                save_weather_data(weather_data)
                api_calls += 1
                if api_calls >= 500:
                    print("Límite diario alcanzado, esperando 24 horas.")
                    sleep(86400)  # Esperar 24 horas
                    api_calls = 0
        current_date = next_date

print("Starting to fetch data")
fetch_data(35.6895, 139.6917)  # Reemplaza con las coordenadas de tu ciudad

cursor.close()
conn.close()
