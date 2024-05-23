# Importaciones necesarias
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer
from sqlalchemy import create_engine
from xgboost import XGBRegressor

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

# Verificar si hay valores NaN después de la imputación
print(f'Número de NaNs en X_train_temp: {np.isnan(X_train_temp).sum()}')
print(f'Número de NaNs en X_test_temp: {np.isnan(X_test_temp).sum()}')

# Paso 2: Definir el modelo y el espacio de búsqueda de hiperparámetros
print("Paso 2: Definiendo el modelo y el espacio de búsqueda de hiperparámetros")

xgb = XGBRegressor(objective='reg:squarederror', random_state=42)

param_dist = {
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 4, 5, 6],
    'learning_rate': [0.01, 0.05, 0.1],
    'subsample': [0.8, 0.9, 1.0],
    'colsample_bytree': [0.8, 0.9, 1.0]
}

# Paso 3: Configurar RandomizedSearchCV
print("Paso 3: Configurando RandomizedSearchCV")

xgb_random = RandomizedSearchCV(estimator=xgb, param_distributions=param_dist, n_iter=20, cv=3, verbose=2, random_state=42, n_jobs=-1)

# Paso 4: Ajustar el modelo a los datos de entrenamiento
print("Paso 4: Ajustando el modelo a los datos de entrenamiento")
xgb_random.fit(X_train_temp, y_train_temp)

# Obtener los mejores hiperparámetros
print("Mejores hiperparámetros encontrados:")
print(xgb_random.best_params_)

# Paso 5: Evaluar el modelo ajustado
print("Paso 5: Evaluando el modelo ajustado")

best_xgb = xgb_random.best_estimator_
y_pred_train_xgb_best = best_xgb.predict(X_train_temp)
y_pred_test_xgb_best = best_xgb.predict(X_test_temp)

train_mse_xgb_best = mean_squared_error(y_train_temp, y_pred_train_xgb_best)
test_mse_xgb_best = mean_squared_error(y_test_temp, y_pred_test_xgb_best)

print(f"Training MSE (Temperature - Best XGBoost): {train_mse_xgb_best}")
print(f"Testing MSE (Temperature - Best XGBoost): {test_mse_xgb_best}")
