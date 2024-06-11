import argparse
from data_loader import load_and_prepare_data, prepare_data, prepare_data_for_rnn
from model_random_forest import train_random_forest
from model_xgboost import train_xgboost
from model_lstm import train_lstm
from model_gru import train_gru

def main(models, days):
    print("Cargando y limpiando los datos")
    df = load_and_prepare_data()
    
    # if models is empty, run all
    if not models:
        models = ['random_forest', 'xgboost', 'lstm', 'gru']
    
    if 'random_forest' in models or 'xgboost' in models:
        print("Preparando datos para modelos basados en árboles")
        X_train, X_test, y_train, y_test = prepare_data(df, 'temperature')

    if 'random_forest' in models:
        print("Entrenando modelo Random Forest")
        train_random_forest(X_train,X_test, y_train, y_test)

    if 'xgboost' in models:
        print("Entrenando modelo XGBoost")
        train_xgboost(X_train, X_test, y_train, y_test)
    
    if 'lstm' in models or 'gru' in models:
        print("Preparando datos para modelos RNN")
        X_rnn, y_rnn = prepare_data_for_rnn(df, 'temperature')

    if 'lstm' in models:
        print("Entrenando modelo LSTM")
        train_lstm(X_rnn, y_rnn, days)
    
    if 'gru' in models:
        print("Entrenando modelo GRU")
        train_gru(X_rnn, y_rnn)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run machine learning models.')
    parser.add_argument('--models', nargs='+', choices=['random_forest', 'xgboost', 'lstm', 'gru'], required=False,
                        help='Specify which models to run: random_forest, xgboost, lstm, gru')
    parser.add_argument('--days', type=int, required=True, help='Specify the number of days to predict')
    args = parser.parse_args()
    main(args.models, args.days)