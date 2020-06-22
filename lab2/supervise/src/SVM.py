import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# solvers.qp() can solve quadprog problem
from cvxopt import solvers, matrix
import math
#  cvxopt.solvers.qp():
#      Solves a quadratic program
#      minimize(1/2)*x'*P*x + q'*x
#      subject to  G*x <= h
#      A*x = b.
class KernelFunc:
    class Linear:
        def val(self, xi:np.array, xj: np.array):
            return np.sum(xi * xj)
    
    class RBF:
        sigma = 1
        def __init__(self, sigma=1): # Constuct Func
            self.sigma = sigma

        def val(self, xi: np.array, xj: np.array):
            return math.exp(-((np.sum((xi - xj) ** 2) ** 0.5) / (self.sigma ** 2)))

def svm_classify(train_set: pd.DataFrame,
                 train_label: pd.DataFrame,
                 test_set: pd.DataFrame,
                 C: float,
                 kernel=KernelFunc.Linear()
                 ):

    print('__svm_classfiy__')
    print(train_set, train_label, test_set, sep='\n')

    train_size = train_set.shape[0]
    x = train_set.to_numpy()
    y = train_label['G3'].to_numpy().astype(float)
    # train_size = 5
    # x = np.array([[1, 2], [2, 3], [3, 3], [2, 1], [3, 2]])
    # y = [1., 1., 1., -1., -1.]
    # print('x: ', x, 'y: ', y, sep='\n')
    P = np.zeros((train_size, train_size))
    for i in range(train_size):
        for j in range(train_size):
            P[i][j] = y[i] * y[j] * kernel.val(x[i], x[j])
    print(P)
    P = matrix(P)
    q = matrix(-np.ones(train_size))
    A = matrix(y, (1, train_size))
    b = matrix(0.)
    G = matrix(np.vstack((-np.eye(train_size), np.eye(train_size))))
    h = matrix(np.hstack((-np.zeros(train_size), C*np.ones(train_size))))
    # print(P, q, A, b, G, h)
    
    sv = solvers.qp(P, q, G, h, A, b)
    result_alpha = np.transpose(np.array(sv['x']))[0]

    cut_value = 1e-6
    result_alpha[result_alpha <= cut_value] = 0
    sv_index = np.where(result_alpha > cut_value)[0]
    print(result_alpha, sv_index, sep='\n')

    result_w = np.zeros(train_set.shape[1])
    
    for i in range(train_size):
        # print(result_alpha[i]*y[i]*x[i])
        result_w += result_alpha[i] * y[i] * x[i]
    print('w:', result_w)

    b = 0
    for i in sv_index:
        # print(i, y[i] - np.sum(result_w * x[i]))
        b += y[i] - np.sum(result_w * x[i])
    b = b / len(sv_index)
    print('b:', b)
    
    # for i in range(train_size):
    #     if y[i] < 0:
    #         plt.plot(x[i][0], x[i][1], 'rx')
    #     else:
    #         plt.plot(x[i][0], x[i][1], 'bo')
    # plot_x = [0., 20.]
    # plot_y = [(-b - result_w[0] * x) / result_w[1] for x in plot_x]
    # print(plot_y)
    # plt.plot(plot_x, plot_y)
    # plt.show()

    # Prediction
    test_arr = test_set.to_numpy()
    predict_arr = np.zeros(test_set.shape[0], dtype=int)
    for i, test_data in enumerate(test_arr):
        predict_arr[i] = 1 if np.sum(result_w * test_data) + b >= 0 else -1
    predict_label = pd.Series(index=test_set.index, data=predict_arr, name="predict")
    print("np.sum(alpha * y) = ",np.sum(result_alpha * y))
    print(predict_label)
    return predict_label