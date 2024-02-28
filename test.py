from sklearn.model_selection import train_test_split
import numpy as np
from sklearn import datasets

iris = datasets.load_iris()

X = np.array(iris.data)
Y = np.array(iris.target)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.25, random_state=0)

print(X_test[2])
print(Y_test[2])
