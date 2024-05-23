import numpy as np

def create_features_and_labels(df, field, n_hours=5):
    X, y = [], []
    for i in range(len(df) - n_hours):
        X.append(df[field].values[i:i + n_hours])
        y.append(df[field].values[i + n_hours])
    return np.array(X), np.array(y)
