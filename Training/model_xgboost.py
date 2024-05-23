from xgboost import XGBRegressor
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import mean_squared_error

def train_xgboost(X_train, X_test, y_train, y_test):
    print("Entrenando XGBoost")
    xgb = XGBRegressor(objective='reg:squarederror', random_state=42)
    param_dist = {
        'n_estimators': [100, 200, 300],
        'max_depth': [3, 4, 5, 6],
        'learning_rate': [0.01, 0.05, 0.1],
        'subsample': [0.8, 0.9, 1.0],
        'colsample_bytree': [0.8, 0.9, 1.0]
    }
    xgb_random = RandomizedSearchCV(estimator=xgb, param_distributions=param_dist, n_iter=20, cv=3, verbose=2, random_state=42, n_jobs=-1)
    xgb_random.fit(X_train, y_train)
    best_xgb = xgb_random.best_estimator_
    y_pred_train = best_xgb.predict(X_train)
    y_pred_test = best_xgb.predict(X_test)
    train_mse = mean_squared_error(y_train, y_pred_train)
    test_mse = mean_squared_error(y_test, y_pred_test)
    print("Mejores hiperparámetros encontrados:", xgb_random.best_params_)
    print(f"Training MSE (Temperature - Best XGBoost): {train_mse}")
    print(f"Testing MSE (Temperature - Best XGBoost): {test_mse}")
