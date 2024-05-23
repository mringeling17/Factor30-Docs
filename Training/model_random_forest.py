from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, TimeoutSampler
from sklearn.metrics import mean_squared_error
import time

def train_random_forest(X_train, X_test, y_train, y_test):
    print("Entrenando Random Forest")
    rf = RandomForestRegressor(random_state=42)

    # Espacio de búsqueda de hiperparámetros
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'bootstrap': [True, False],
        'max_features': ['auto', 'sqrt']
    }

    # Uso de GridSearchCV con TimeoutSampler
    timeout_sampler = TimeoutSampler(timeout=60)  # Timeout de 60 segundos por configuración
    grid_search_rf = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, verbose=2, n_jobs=-1, pre_dispatch=timeout_sampler)

    # Ajustar el modelo a los datos de entrenamiento
    start_time = time.time()
    grid_search_rf.fit(X_train, y_train)
    end_time = time.time()
    print(f"Tiempo total de ejecución: {end_time - start_time:.2f} segundos")

    # Obtener los mejores hiperparámetros
    best_rf = grid_search_rf.best_estimator_
    print("Mejores hiperparámetros encontrados:", grid_search_rf.best_params_)

    # Evaluar el modelo ajustado
    y_pred_train = best_rf.predict(X_train)
    y_pred_test = best_rf.predict(X_test)
    train_mse = mean_squared_error(y_train, y_pred_train)
    test_mse = mean_squared_error(y_test, y_pred_test)

    print(f"Training MSE (Temperature - Best Random Forest): {train_mse}")
    print(f"Testing MSE (Temperature - Best Random Forest): {test_mse}")

# Ejemplo de uso de la función (asegúrate de que X_train, X_test, y_train, y_test estén definidos)
# train_random_forest(X_train_temp, X_test_temp, y_train_temp, y_test_temp)
