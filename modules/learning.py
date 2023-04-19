import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_absolute_error


def lgb_regression(df):
    df_train, df_test = train_test_split(df, test_size=0.2)

    col = 'distance'

    train_y, train_x = df_train[col], df_train.drop(col, axis=1)
    test_y, test_x = df_test[col], df_test.drop(col, axis=1)

    trains = lgb.Dataset(train_x, train_y)
    tests = lgb.Dataset(test_x, test_y)

    params = {
        'objective': 'regression',
        'metrics': 'mae',
        'num_leaves': 31
    }

    return lgb.train(params,
                      trains,
                      valid_sets=tests,
                      num_boost_round=1000,
                      early_stopping_rounds=100)


def sgd_regression(df):
    X_train, X_test, y_train, y_test = train_test_split(df.drop('distance', axis=1), df['distance'], test_size=0.2, random_state=42)
    X_train, X_test = standardization(X_train, X_test)

    sgd_reg = SGDRegressor(max_iter=1000, tol=1e-3, penalty=None, eta0=0.1, random_state=42)
    sgd_reg.fit(X_train, y_train)

    return sgd_reg


def standardization(x_train, x_test):
    sc = StandardScaler()
    sc.fit(x_train)

    return sc.transform(x_train), sc.transform(x_test)