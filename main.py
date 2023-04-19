from modules import preprocessing, making_figures, learning, predicting
import pandas as pd
import numpy as np


def main():
    print('Start processing...')

    processing_type = int(input('Enter 0 if you have already processed data, or 1 if you want to start from data processing:'))

    df = None

    if processing_type == 1:
        df = preprocessing.get_and_save_dataframe()
    elif processing_type == 0:
        df = pd.read_csv('data/preprocessed_data.csv')

    df = preprocessing.drop_unnecessary_columns(df)
    df.corr().to_csv('data/corr.csv')

    making_figures.make_scatter(df, 'Time and Distance Relationships(Tokyo-Destination)', 'distance', 'Distance[km]', 'travel_time', 'Time[minute]')


    gbm = learning.lgb_regression(df)
    predicting.predict(gbm)

    print('Finish.')


if __name__ == '__main__':
    main()
