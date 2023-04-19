from modules import preprocessing, making_figures, learning, predicting
import pandas as pd


def main():
    print('Start processing...')
    inputted = int(input('Enter 0 if you have already processed data, or 1 if you want to start from data processing:'))

    df = []

    if inputted == 1:
        df = preprocessing.get_and_save_dataframe()

    if inputted == 0:
        df = pd.read_csv('data/preprocessed_data.csv')

    df = preprocessing.drop_unnecessary_columns(df)
    print(df)
    making_figures.make_scatter(df, 'Time and Distance Relationships(Tokyo-Destination)', 'distance', 'Distance[km]', 'travel_time', 'Time[minute]')

    model = learning.lgb_regression(df)

    print(model)


if __name__ == '__main__':
    main()
