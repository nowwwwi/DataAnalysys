import pandas as pd


def predict(gbm_model):
    df = pd.read_csv('data/prediction.csv')

    destination_lis = df['destination']
    prediction_lis = df.drop(['destination'], axis=1)
    predict_results = pd.DataFrame(gbm_model.predict(prediction_lis), columns=['travel_time'])
    df_result = pd.concat([destination_lis, pd.DataFrame(predict_results)], axis=1)

    df_result.to_csv('data/result.csv')

