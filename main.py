from modules import preprocessing, making_figures, learning, predicting
import pandas as pd


def main():
    print('Start processing...')

    processing_type = int(input('Input any key if you have already processed data, or 1 if you want to start from data processing:'))

    df = preprocessing.preprocess() if processing_type == 1 else pd.read_csv('data/cleansed_data.csv')

    print(df.dtypes)

    processing_type = int(input('Enter 1 if you want to write figure and corr table.:'))

    if processing_type == 1:
        df.corr().to_csv('data/corr.csv')
        making_figures.make_scatter(df)
    else:
        pass

    gbm = learning.lgb_regression(df)
    predicting.predict(gbm)

    print('Finish.')


if __name__ == '__main__':
    main()
