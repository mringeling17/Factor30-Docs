import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from utils import create_features_and_labels

# Cargar las variables de entorno
load_dotenv()

def load_and_prepare_data():
    print("Cargando y limpiando los datos")
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_PORT = os.getenv('DB_PORT')
    engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    query = "SELECT * FROM weather_data"
    df = pd.read_sql(query, engine)
    df['date_time'] = pd.to_datetime(df['date_time'])
    df.set_index('date_time', inplace=True)
    df = df.sort_index()
    return df

def prepare_data(df, field):
    X, y = create_features_and_labels(df, field)
    from sklearn.impute import SimpleImputer
    from sklearn.model_selection import train_test_split

    imputer = SimpleImputer(strategy='mean')
    X = imputer.fit_transform(X)
    y = imputer.fit_transform(y.reshape(-1, 1)).ravel()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    return X_train, X_test, y_train, y_test
