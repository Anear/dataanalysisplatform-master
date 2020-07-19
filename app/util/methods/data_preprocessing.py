# _*_ coding: UTF-8 _*_

from sklearn.preprocessing import scale
import numpy as np


def scaled(X,axis1 = 0):
    X = scale(X, axis=axis1)
    return X


def diff(X, periods1=1, drop=True):
    if drop:
        X_diff = X.diff(periods=periods1).dropna()
    else:
        X_diff = X.diff(periods=periods1)
    return X_diff


def log_data(X):
    X_log = np.log2(X)
    return X_log
