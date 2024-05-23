# Importaciones necesarias
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import RandomizedSearchCV

# Paso 1: Cargar y limpiar los datos
print("Paso 1: Cargando y limpiando los datos")

# Configuración de la base de datos
DB_HOST = 'aws-0-eu-central-1.pooler.supabase.com'
DB_NAME = 'postgres'
DB_USER = 'postgres.karyjqxvursphmmomvky'
DB_PASSWORD = 'i1mQWy0EzJHz27Pd'
DB_PORT = '5432' 

# Crear la conexión usando SQLAlchemy
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Cargar los datos en un DataFrame
query = "SELECT * FROM weather_data"
df = pd.read_sql(query, engine)

# Convertir la columna de fecha y hora a datetime
df['date_time'] = pd.to_datetime(df['date_time'])
df.set_index('date_time', inplace=True)
df = df.sort_index()

# Crear las características y etiquetas para la temperatura
def create_features_and_labels(df, field, n_hours=5):
    X, y = [], []
    for i in range(len(df) - n_hours):
        X.append(df[field].values[i:i + n_hours])
        y.append(df[field].values[i + n_hours])
    return np.array(X), np.array(y)

# Características y etiquetas para la temperatura
X_temp, y_temp = create_features_and_labels(df, 'temperature')

# Imputar cualquier valor NaN en las características
imputer = SimpleImputer(strategy='mean')
X_temp = imputer.fit_transform(X_temp)

# Imputar cualquier valor NaN en las etiquetas si es necesario
y_temp = imputer.fit_transform(y_temp.reshape(-1, 1)).ravel()

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train_temp, X_test_temp, y_train_temp, y_test_temp = train_test_split(X_temp, y_temp, test_size=0.3, random_state=42)

# Escalar los datos
scaler = StandardScaler()
X_train_temp = scaler.fit_transform(X_train_temp)
X_test_temp = scaler.transform(X_test_temp)

# Redimensionar los datos para LSTM
X_train_temp = X_train_temp.reshape((X_train_temp.shape[0], X_train_temp.shape[1], 1))
X_test_temp = X_test_temp.reshape((X_test_temp.shape[0], X_test_temp.shape[1], 1))

# Paso 2: Definir el modelo de LSTM
def create_model(optimizer='adam', units=50, dropout_rate=0.2, learning_rate=0.001):
    model = Sequential()
    model.add(LSTM(units=units, activation='relu', input_shape=(X_train_temp.shape[1], 1), return_sequences=True))
    model.add(Dropout(dropout_rate))
    model.add(LSTM(units=units, activation='relu'))
    model.add(Dropout(dropout_rate))
    model.add(Dense(1))
    optimizer = Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss='mse')
    return model

# Paso 3: Configurar RandomizedSearchCV
print("Paso 3: Configurando RandomizedSearchCV")

model = KerasRegressor(build_fn=create_model, verbose=0)

param_dist = {
    'units': [50, 100, 150],
    'dropout_rate': [0.2, 0.3, 0.4],
    'batch_size': [16, 32, 64],
    'epochs': [50, 100, 150],
    'learning_rate': [0.001, 0.005, 0.01]
}

random_search = RandomizedSearchCV(estimator=model, param_distributions=param_dist, n_iter=20, cv=2, verbose=2, random_state=42, n_jobs=1)

# Paso 4: Ajustar el modelo a los datos de entrenamiento
print("Paso 4: Ajustando el modelo a los datos de entrenamiento")
random_search.fit(X_train_temp, y_train_temp)

# Obtener los mejores hiperparámetros
print("Mejores hiperparámetros encontrados:")
print(random_search.best_params_)

# Paso 5: Evaluar el modelo ajustado
print("Paso 5: Evaluando el modelo ajustado")

best_model = random_search.best_estimator_
y_pred_train_lstm_best = best_model.predict(X_train_temp)
y_pred_test_lstm_best = best_model.predict(X_test_temp)

train_mse_lstm_best = mean_squared_error(y_train_temp, y_pred_train_lstm_best)
test_mse_lstm_best = mean_squared_error(y_test_temp, y_pred_test_lstm_best)

print(f"Training MSE (Temperature - Best LSTM): {train_mse_lstm_best}")
print(f"Testing MSE (Temperature - Best LSTM): {test_mse_lstm_best}")
