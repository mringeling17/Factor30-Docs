# model_tft.py

import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tft_model import TemporalFusionTransformer
from utils import create_features_and_labels_tft

def prepare_data_for_tft(df, field, sequence_length=5):
    X, y = create_features_and_labels_tft(df, field)
    
    # Verificar valores NaN o Inf antes de la normalización
    if np.isnan(X).any() or np.isinf(X).any():
        print("Datos originales de características contienen NaN o Inf.")
    if np.isnan(y).any() or np.isinf(y).any():
        print("Datos originales de etiquetas contienen NaN o Inf.")
    
    # Reemplazar valores NaN o Inf por la media de cada columna
    X = np.nan_to_num(X, nan=np.nanmean(X))
    X = np.where(np.isinf(X), np.nanmean(X), X)
    y = np.nan_to_num(y, nan=np.nanmean(y))
    y = np.where(np.isinf(y), np.nanmean(y), y)

    print(f"Tamaño de X: {X.shape}, Tamaño de y: {y.shape}")
    
    num_features = X.shape[1] // sequence_length
    if num_features == 0:
        raise ValueError("El número de características es insuficiente para crear secuencias de 5 pasos.")
    
    print(f"Número de características: {num_features}")
    
    X = X.reshape(-1, sequence_length, num_features)
    return X, y

def train_tft(X, y):
    # Dividir los datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Normalizar los datos
    scaler = StandardScaler()
    X_train_reshaped = X_train.reshape(-1, X_train.shape[-1])
    X_test_reshaped = X_test.reshape(-1, X_test.shape[-1])
    X_train_scaled = scaler.fit_transform(X_train_reshaped).reshape(X_train.shape)
    X_test_scaled = scaler.transform(X_test_reshaped).reshape(X_test.shape)

    # Verificar datos después de la normalización
    if np.isnan(X_train_scaled).any() or np.isinf(X_train_scaled).any():
        raise ValueError("Datos de entrenamiento contienen NaN o Inf después de la normalización.")
    if np.isnan(X_test_scaled).any() or np.isinf(X_test_scaled).any():
        raise ValueError("Datos de prueba contienen NaN o Inf después de la normalización.")
    if np.isnan(y_train).any() or np.isinf(y_train).any():
        raise ValueError("Etiquetas de entrenamiento contienen NaN o Inf.")
    if np.isnan(y_test).any() or np.isinf(y_test).any():
        raise ValueError("Etiquetas de prueba contienen NaN o Inf.")

    # Crear el modelo TFT
    model = TemporalFusionTransformer(
        hidden_layer_size=64,
        dropout_rate=0.1,
        learning_rate=0.0001,  # Reduje la tasa de aprendizaje
        num_heads=4,
        num_encoder_steps=5,  # Cambié la longitud de la secuencia a 5
        num_decoder_steps=5,  # Cambié la longitud de la secuencia a 5
        output_size=1,
        batch_first=True
    )

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001), loss='mse')

    # Entrenar el modelo
    model.fit(X_train_scaled, y_train, epochs=100, batch_size=64, validation_data=(X_test_scaled, y_test))

    # Evaluar el modelo
    loss = model.evaluate(X_test_scaled, y_test)
    print(f'MSE en testing: {loss}')