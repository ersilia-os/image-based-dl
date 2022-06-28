import os
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import RobustScaler

'Nan Filtering'
MAX_NA = 0.2
class NanFilter(object):
    def __init__(self):
        self._name = "nan_filter"

    def fit(self, X):
        max_na = int((1 - MAX_NA) * X.shape[0])
        idxs = []
        for j in range(X.shape[1]):
            c = np.sum(np.isnan(X[:, j]))
            if c > max_na:
                continue
            else:
                idxs += [j]
        self.col_idxs = idxs
        print(
            "Nan filtering, original columns {0}, final columns {1}".format(
                X.shape[1], len(self.col_idxs)
            )
        )

    def transform(self, X):
        return X[:, self.col_idxs]

    def save(self, file_path, file_name):
        joblib.dump(self, (os.path.join(file_path, file_name)))

    def load(self, file_path, file_name):
        return joblib.load(os.path.join(file_path, file_name))

'Imputer'
class Imputer(object):
    def __init__(self):
        self._name = "imputer"
        self._fallback = 0

    def fit(self, X):
        ms = []
        for j in range(X.shape[1]):
            vals = X[:, j]
            mask = ~np.isnan(vals)
            vals = vals[mask]
            if len(vals) == 0:
                m = self._fallback
            else:
                m = np.median(vals)
            ms += [m]
        self.impute_values = np.array(ms)

    def transform(self, X):
        for j in range(X.shape[1]):
            mask = np.isnan(X[:, j])
            X[mask, j] = self.impute_values[j]
        return X

    def save(self, file_path, file_name):
        joblib.dump(self, (os.path.join(file_path, file_name)))

    def load(self, file_path, file_name):
        return joblib.load(os.path.join(file_path, file_name))

'Scaler'
class Scaler(object):
    def __init__(self):
        self._name = "scaler"
        self.abs_limit = 10
        self.skip = False

    def set_skip(self):
        self.skip = True

    def fit(self, X):
        if self.skip:
            return
        self.scaler = RobustScaler()
        self.scaler.fit(X)

    def transform(self, X):
        if self.skip:
            return X
        X = self.scaler.transform(X)
        X = np.clip(X, -self.abs_limit, self.abs_limit)
        return X
    
    def save(self, file_path, file_name):
        joblib.dump(self, (os.path.join(file_path, file_name)))

    def load(self, file_path, file_name):
        return joblib.load(os.path.join(file_path, file_name))

