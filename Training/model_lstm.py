import numpy as np
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import RandomizedSearchCV, train_test_split

def create_model(input_shape, optimizer='adam', units=50, dropout_rate=0.2, learning_rate=0.001):
    model = Sequential()
    model.add(LSTM(units=units, activation='relu', input_shape=input_shape, return_sequences=True))
    model.add(Dropout(dropout_rate))
    model.add(LSTM(units=units, activation='relu'))
    model.add(Dropout(dropout_rate))
    model.add(Dense(1))
    optimizer = Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss='mse')
    return model

def train_lstm(X, y, days):
    print("Entrenando LSTM")

    # Dividir los datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    input_shape = (X_train.shape[1], X_train.shape[2])
    model = KerasRegressor(build_fn=create_model, input_shape=input_shape, verbose=1)

    param_dist = {
        'units': [50, 100, 150],
        'dropout_rate': [0.2, 0.3, 0.4],
        'batch_size': [16, 32, 64],
        'epochs': [50, 100, 150],
        'learning_rate': [0.001, 0.005, 0.01]
    }

    print("Iniciando búsqueda de hiperparámetros")
    random_search = RandomizedSearchCV(estimator=model, param_distributions=param_dist, n_iter=20, cv=2, verbose=2, random_state=42, n_jobs=1)

    random_search.fit(X_train, y_train)
    print("Búsqueda de hiperparámetros completada")

    best_model = random_search.best_estimator_
    print("Mejores hiperparámetros encontrados:", random_search.best_params_)

    y_pred_train_lstm_best = best_model.predict(X_train)
    y_pred_test_lstm_best = best_model.predict(X_test)

    train_mse_lstm_best = mean_squared_error(y_train, y_pred_train_lstm_best)
    test_mse_lstm_best = mean_squared_error(y_test, y_pred_test_lstm_best)

    print(f"Training MSE (Temperature - Best LSTM): {train_mse_lstm_best}")
    print(f"Testing MSE (Temperature - Best LSTM): {test_mse_lstm_best}")

    # Realizar predicción para los próximos `days` días
    last_sequence = X[-1]  # Utilizar la última secuencia del conjunto completo de datos
    predictions = []
    for _ in range(days):
        pred = best_model.predict(last_sequence.reshape(1, *last_sequence.shape))
        predictions.append(pred[0][0])  # Añadir solo el valor predicho, no el array
        last_sequence = np.roll(last_sequence, -1, axis=0)
        last_sequence[-1] = pred

    print(f"Predicción para los próximos {days} días:", predictions)