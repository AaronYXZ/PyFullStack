import numpy as np
import math
from sklearn import datasets

def load_data():
    # load iris data from sklearn.datasets
    # return X as a n by 3 array and y as a binary (0,1) array
    iris = datasets.load_iris()
    X = iris.data[:, :2]
    y = (iris.target != 0) * 1
    np.random.seed(1)
    np.random.shuffle(X)
    np.random.seed(1)
    np.random.shuffle(y)
    train_size = int(X.shape[0] * 0.8)

    X_train = X[:train_size]
    y_train = y[:train_size]
    X_test = X[train_size:]
    y_test = y[train_size:]
    return X_train, y_train, X_test, y_test

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def cost(w, b, X, Y):
    m = X.shape[1]
    A = sigmoid(np.dot(w.T, X) + b)
    c =  - (np.sum(np.dot(np.log(A), Y.T)) + np.sum(np.dot(np.log(1-A) ,(1-Y.T)))) / m
    return c

def gradient_descent(w, b, X, Y):
    """
    :param w: weight matrix, shape of [n, 1] n being the number of parameters
    :param b: bias, a scalar value
    :param X: input matrix, shape of [n, m] n being the number of features/parameters, m being number of records in X
    :param Y: vector, shape of [1, m], label of x, m being number of records in Y
    :return: dw and db, gradients of w and b, dw shape of [n, 1], db a scalar value
    """
    m = X.shape[1] # number of data points in X
    A = sigmoid(np.dot(w.T, X) + b) # A shape of [1, m]
    dw = np.dot(X, (A-Y).T) / m # use np.dot(X, (A-y).T) cause this will make shape of dw correct. dw is
    db = np.sum(A - Y) / m
    return dw, db


def train(X, y, iteration = 2000, learning_rate = 0.01):
    w = np.zeros((X.shape[0], 1))
    b = 0
    for i in range(iteration):
        dw, db = gradient_descent(w, b, X, y)
        w  = w - learning_rate * dw
        b = b - learning_rate * db
    c = cost(w, b, X, y)
    return w, b, c

def predict(w, b, X, y):
    z = np.dot(w.T, X) + b
    y_predict = (sigmoid(z) > 0.5) * 1
    c = cost(w, b, X, y)
    return y_predict, c





if __name__ == '__main__':
    X_train, y_train, X_test, y_test = load_data()
    X_train = X_train.T
    X_test = X_test.T
    y_train = y_train.reshape(1, -1)
    y_test = y_test.reshape(1, -1)
    w, b, _ = train(X_train, y_train)
    y_predict, _ = predict(w, b, X_test, y_test)
    print(y_predict)
    print(y_test)
    size = X_test.shape[1]
    errors = np.sum([1 for i in range(size) if y_test[0][i] != y_predict[0][i]])
    print("Precision is {:6.2f}".format(1 - errors/size))