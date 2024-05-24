from xgboost import XGBRegressor
from sklearn.model_selection import RandomizedSearchCV, cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, median_absolute_error
import numpy as np

def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    non_zero_indices = y_true != 0
    return np.mean(np.abs((y_true[non_zero_indices] - y_pred[non_zero_indices]) / y_true[non_zero_indices])) * 100

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
    test_rmse = np.sqrt(test_mse)
    test_mae = mean_absolute_error(y_test, y_pred_test)
    test_r2 = r2_score(y_test, y_pred_test)
    test_mape = mean_absolute_percentage_error(y_test, y_pred_test)
    test_medae = median_absolute_error(y_test, y_pred_test)
    
    print("Mejores hiperparámetros encontrados:", xgb_random.best_params_)
    print(f"Training MSE: {train_mse}")
    print(f"Testing MSE: {test_mse}")
    print(f"Testing RMSE: {test_rmse}")
    print(f"Testing MAE: {test_mae}")
    print(f"Testing R²: {test_r2}")
    print(f"Testing MAPE: {test_mape}")
    print(f"Testing MedAE: {test_medae}")
    
    cv_scores = cross_val_score(best_xgb, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
    cv_mse = -cv_scores.mean()
    print(f"Cross-Validation MSE: {cv_mse}")
