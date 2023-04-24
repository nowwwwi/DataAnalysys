from modules import preprocessing, making_figures, learning, predicting
import pandas as pd
import lightgbm as lgb


def main():
    print('Start processing...')

    processing_type = int(input('Input any key if you have already processed data, or 1 if you want to start from data processing:'))

    df = preprocessing.preprocess() if processing_type == 1 else preprocessing.clean_and_save_dataframe(pd.read_csv('data/temp_data.csv'))

    processing_type = int(input('Enter 1 if you want to write figure and corr table.:'))

    if processing_type == 1:
        # df.corr().to_csv('data/corr.csv')
        making_figures.make_scatter(df)
    else:
        pass

    processing_type = int(
        input('Enter 0 to load a trained model or 1 to start with training data: '))

    model = lgb.Booster(model_file='/data/model.txt') if processing_type == 1 else learning.lgb_regression(df)

    predicting.predict(model)

    print('Finish.')


if __name__ == '__main__':
    main()
