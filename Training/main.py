import argparse
from data_loader import load_and_prepare_data, prepare_data
from model_random_forest import train_random_forest
from model_xgboost import train_xgboost
from model_lstm import train_lstm

def main(models):
    df = load_and_prepare_data()
    X_train, X_test, y_train, y_test = prepare_data(df, 'temperature')

    #if models is empty, run all
    if not models:
        models = ['random_forest', 'xgboost', 'lstm']

    if 'random_forest' in models:
        train_random_forest(X_train, X_test, y_train, y_test)

    if 'xgboost' in models:
        train_xgboost(X_train, X_test, y_train, y_test)
    
    if 'lstm' in models:
        train_lstm(X_train, X_test, y_train, y_test)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run machine learning models.')
    parser.add_argument('--models', nargs='+', choices=['random_forest', 'xgboost', 'lstm'], required=False,
                        help='Specify which models to run: random_forest, xgboost, lstm')
    args = parser.parse_args()
    main(args.models)
