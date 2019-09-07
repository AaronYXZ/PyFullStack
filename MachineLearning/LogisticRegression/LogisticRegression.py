import numpy as np

class LogisticRegression:
    def __init__(self ):
        pass

    def fit(self, X, Y):
        if not isinstance(X, np.ndarray):
            raise TypeError("X must be an array")

        self._w, self._b = self._train(X, Y)

    def predict(self, X):
        if self._w == None or self._b == None:
            raise TypeError("Model hasn't been trained yet")