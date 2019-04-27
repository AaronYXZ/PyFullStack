from sklearn.naive_bayes import MultinomialNB
import pandas as pd
import numpy as np

data = pd.read_csv("resources/spambase.data").as_matrix()
np.random.shuffle(data)

X = data[:, :48]
Y = data[:, -1]
# print(data.shape)

Xtrain = X[:-100, ]
Ytrain = Y[:-100, ]
Xtest = X[-100:, ]
Ytest = Y[-100:, ]

model = MultinomialNB()
model.fit(Xtrain, Ytrain)
score = model.score(Xtest, Ytest)
print(score)

from sklearn.ensemble import AdaBoostClassifier

model2 = AdaBoostClassifier()
model2.fit(Xtrain, Ytrain)
score = model2.score(Xtest, Ytest)
print(score)