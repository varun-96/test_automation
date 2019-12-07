import os.path as op
import numpy as np
import pandas as pd

from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
from configparser import ConfigParser

def get_config():
    """
    Read configuration file and returns it as an ordered Dict'

    Returns
    ------
    config : Ordered Dict
        contains parameter values for each file

    """
    config = ConfigParser()
    config.read(op.join(op.dirname(op.abspath(__file__)), "config.ini"))
    return config


cfg = get_config()

def train():
    """ Train ML model on IRIS data set"""
    data = pd.read_csv(cfg.get('train', 'data_path'))

    # Hyperparameters
    penalty = cfg.get('train', 'penalty')
    tol = cfg.getfloat('train', 'tol')
    max_iter = cfg.getint('train', 'max_iter')

    X = data.drop(['Id', 'Species'], axis=1)
    y = data['Species']
    print(X.shape)
    print(y.shape)

    logreg = LogisticRegression(penalty=penalty, tol=tol, max_iter=max_iter)
    logreg.fit(X, y)
    y_pred = logreg.predict(X)
    print(metrics.accuracy_score(y, y_pred))

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=5)
    print(X_train.shape)
    print(y_train.shape)
    print(X_test.shape)
    print(y_test.shape)

    joblib.dump(logreg, cfg.get('train', 'model_path'))


if __name__ == "__main__":
    train()