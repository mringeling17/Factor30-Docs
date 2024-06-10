import numpy as np

def create_features_and_labels(df, field, n_hours=5):
    X, y = [], []
    for i in range(len(df) - n_hours):
        X.append(df[field].values[i:i + n_hours])
        y.append(df[field].values[i + n_hours])
    return np.array(X), np.array(y)

# utils.py

# utils.py

def create_features_and_labels_tft(df, field):
    X = df.drop(columns=[field]).values
    
    # Verifica el tamaño de X después de eliminar la columna objetivo
    print(f"Tamaño de X después de eliminar {field}: {X.shape}")
    
    y = df[field].values
    return X, y