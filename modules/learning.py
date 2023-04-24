import lightgbm as lgb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def lgb_regression(df: pd.DataFrame):
    df_train, df_test = train_test_split(df, test_size=0.3)

    col = 'travel_time'

    train_y, train_x = df_train[col], df_train.drop(col, axis=1)
    test_y, test_x = df_test[col], df_test.drop(col, axis=1)

    trains = lgb.Dataset(train_x, train_y)
    tests = lgb.Dataset(test_x, test_y)

    params = {
        'objective': 'regression',
        'metrics': 'mae',
        'num_leaves': 31
    }

    model = lgb.train(params, trains, valid_sets=tests, num_boost_round=10000, early_stopping_rounds=1000)
    model.save_model('data/model.txt', num_iteration=model.best_iteration)

    return model


def standardization(x_train, x_test):
    sc = StandardScaler()
    sc.fit(x_train)

    return sc.transform(x_train), sc.transform(x_test)