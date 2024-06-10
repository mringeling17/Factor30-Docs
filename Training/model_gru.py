import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split

def train_gru(X_train, X_test, y_train, y_test):
    # Definir los parámetros del modelo
    sequence_length = X_train.shape[1]
    n_features = X_train.shape[2]

    # Normalizar los datos
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X_train_reshaped = X_train.reshape(-1, n_features)
    X_test_reshaped = X_test.reshape(-1, n_features)
    X_train_scaled = scaler.fit_transform(X_train_reshaped).reshape(X_train.shape)
    X_test_scaled = scaler.transform(X_test_reshaped).reshape(X_test.shape)

    # Crear el modelo
    model = Sequential()
    model.add(GRU(units=64, return_sequences=True, input_shape=(sequence_length, n_features), kernel_regularizer='l2'))
    model.add(Dropout(0.3))
    model.add(BatchNormalization())
    model.add(GRU(units=64, return_sequences=False, kernel_regularizer='l2'))
    model.add(Dropout(0.3))
    model.add(BatchNormalization())
    model.add(Dense(units=1))

    # Compilar el modelo con un learning rate reducido
    optimizer = Adam(learning_rate=0.001)
    model.compile(optimizer=optimizer, loss='mean_squared_error')

    # Definir early stopping y reducción del learning rate al estancamiento
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=0.00001)

    # Entrenar el modelo con early stopping y reducción del learning rate
    model.fit(X_train_scaled, y_train, epochs=100, batch_size=64, validation_data=(X_test_scaled, y_test), callbacks=[early_stopping, reduce_lr])

    # Evaluar el modelo
    loss = model.evaluate(X_test_scaled, y_test)
    print(f'MSE en testing: {loss}')