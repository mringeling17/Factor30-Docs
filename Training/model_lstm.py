import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import RandomizedSearchCV

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

def train_lstm(X_train, X_test, y_train, y_test):
    print("Entrenando LSTM")
    
    # Escalar los datos
    scaler = StandardScaler()
    X_train_temp = scaler.fit_transform(X_train)
    X_test_temp = scaler.transform(X_test)

    # Redimensionar los datos para LSTM
    X_train_temp = X_train_temp.reshape((X_train_temp.shape[0], X_train_temp.shape[1], 1))
    X_test_temp = X_test_temp.reshape((X_test_temp.shape[0], X_test_temp.shape[1], 1))

    input_shape = (X_train_temp.shape[1], 1)
    model = KerasRegressor(build_fn=create_model, input_shape=input_shape, verbose=0)

    param_dist = {
        'units': [50, 100, 150],
        'dropout_rate': [0.2, 0.3, 0.4],
        'batch_size': [16, 32, 64],
        'epochs': [50, 100, 150],
        'learning_rate': [0.001, 0.005, 0.01]
    }

    random_search = RandomizedSearchCV(estimator=model, param_distributions=param_dist, n_iter=20, cv=2, verbose=2, random_state=42, n_jobs=1)

    random_search.fit(X_train_temp, y_train)

    best_model = random_search.best_estimator_
    y_pred_train_lstm_best = best_model.predict(X_train_temp)
    y_pred_test_lstm_best = best_model.predict(X_test_temp)

    train_mse_lstm_best = mean_squared_error(y_train, y_pred_train_lstm_best)
    test_mse_lstm_best = mean_squared_error(y_test, y_pred_test_lstm_best)

    print("Mejores hiperparámetros encontrados:", random_search.best_params_)
    print(f"Training MSE (Temperature - Best LSTM): {train_mse_lstm_best}")
    print(f"Testing MSE (Temperature - Best LSTM): {test_mse_lstm_best}")
