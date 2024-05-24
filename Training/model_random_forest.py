from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, median_absolute_error
import numpy as np

def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    non_zero_indices = y_true != 0
    return np.mean(np.abs((y_true[non_zero_indices] - y_pred[non_zero_indices]) / y_true[non_zero_indices])) * 100

def train_random_forest(X_train, X_test, y_train, y_test):
    print("Entrenando Random Forest")
    best_params = {
        'bootstrap': True,
        'max_depth': 30,
        'max_features': 'sqrt',
        'min_samples_leaf': 2,
        'min_samples_split': 10,
        'n_estimators': 300
    }
    
    rf = RandomForestRegressor(**best_params, random_state=42)
    rf.fit(X_train, y_train)
    
    y_pred_train = rf.predict(X_train)
    y_pred_test = rf.predict(X_test)
    
    train_mse = mean_squared_error(y_train, y_pred_train)
    test_mse = mean_squared_error(y_test, y_pred_test)
    test_rmse = np.sqrt(test_mse)
    test_mae = mean_absolute_error(y_test, y_pred_test)
    test_r2 = r2_score(y_test, y_pred_test)
    test_mape = mean_absolute_percentage_error(y_test, y_pred_test)
    test_medae = median_absolute_error(y_test, y_pred_test)
    
    print("Mejores hiperparámetros utilizados:", best_params)
    print(f"Training MSE: {train_mse}")
    print(f"Testing MSE: {test_mse}")
    print(f"Testing RMSE: {test_rmse}")
    print(f"Testing MAE: {test_mae}")
    print(f"Testing R²: {test_r2}")
    print(f"Testing MAPE: {test_mape}")
    print(f"Testing MedAE: {test_medae}")
    
    cv_scores = cross_val_score(rf, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
    cv_mse = -cv_scores.mean()
    print(f"Cross-Validation MSE: {cv_mse}")
