# main.py

import argparse
from data_loader import load_and_prepare_data, prepare_data, prepare_data_for_rnn
from model_random_forest import train_random_forest
from model_xgboost import train_xgboost
from model_lstm import train_lstm
from model_gru import train_gru
from model_tft import train_tft, prepare_data_for_tft

def main(models):
    df = load_and_prepare_data()
    
    if not models:
        models = ['random_forest', 'xgboost', 'lstm', 'gru']
    
    if 'random_forest' in models or 'xgboost' in models:
        X_train, X_test, y_train, y_test = prepare_data(df, 'temperature')

    if 'random_forest' in models:
        train_random_forest(X_train, X_test, y_train, y_test)

    if 'xgboost' in models:
        train_xgboost(X_train, X_test, y_train, y_test)
    
    if 'lstm' in models or 'gru' in models:
        X_train_rnn, X_test_rnn, y_train_rnn, y_test_rnn = prepare_data_for_rnn(df, 'temperature')

    if 'lstm' in models:
        train_lstm(X_train_rnn, X_test_rnn, y_train_rnn, y_test_rnn)
    
    if 'gru' in models:
        train_gru(X_train_rnn, X_test_rnn, y_train_rnn, y_test_rnn)

    # if 'tft' in models:
    #     X_tft, y_tft = prepare_data_for_tft(df, 'temperature')
    #     train_tft(X_tft, y_tft)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run machine learning models.')
    parser.add_argument('--models', nargs='+', choices=['random_forest', 'xgboost', 'lstm', 'gru'], required=False,
                        help='Specify which models to run: random_forest, xgboost, lstm, gru')
    #if no arguments are provided, all models will be run and make a print saying that
    args = parser.parse_args()
    if not args.models:
        print("No models specified, running all models.")
    main(args.models)