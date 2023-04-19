from sklearn.metrics import accuracy_score


def prediction(model, test_x, test_y):
    pred_y = model.predict(test_x, num_iteration=model.best_iteration)
    return pred_y, accuracy_score(test_y, pred_y)

