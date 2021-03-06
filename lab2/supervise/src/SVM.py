import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# solvers.qp() can solve quadprog problem

from cvxopt import solvers, matrix

#  cvxopt.solvers.qp():
#      Solves a quadratic program
#      minimize(1/2)*x'*P*x + q'*x
#      subject to  G*x <= h
#      A*x = b.

import math


class KernelFunc:
    """
    KernelFunc:
        Defines 3 types of kernel functions.
    """

    class Linear:
        """
        linear kernel: K(xi, xj) = xi * xj (* = \cdot)
        """
        name = "Linear"
        def val(self, xi: np.array, xj: np.array):
            return np.sum(xi * xj)

    class RBF:
        """
        rbf kernel: K(xi, xj) = exp{||xi - xj|| / sigma^2}
        """
        sigma = 1
        name = "RBF: "
        def __init__(self, sigma=1):  # Constuct Func
            self.sigma = sigma
            self.name += "sigma = %f" % self.sigma

        def val(self, xi: np.array, xj: np.array):
            return math.exp(-(np.sum((xi - xj) ** 2) ** 0.5 / (self.sigma ** 2)))

    class Poly:
        """
        Polynomial kernel: K(xi, xj) = (xi * xj + c)^d (* = \cdot)
        """
        d = 2  # default: square
        c = 0
        name = "Polynomial: "
        def __init__(self, d=2, c=0):
            self.d, self.c = d, c
            self.name += "d = %d, c = %d" % (d, c)

        def val(self, xi: np.array, xj: np.array):
            return (np.sum(xi * xj) + self.c) ** self.d
        
def svm_classify(train_set: pd.DataFrame,
                 train_label: pd.DataFrame,
                 test_set: pd.DataFrame,
                 C: float,
                 kernel=KernelFunc.Linear(),
                 cut_value=0
                 ):
    """
    SVM Classify Function:

    input args:
        train_set, train_label, test_set, C;

        kernel:
            Type of kernel function.
            the value can be one of those:
                KernelFunc.Linear()
                KernelFunc.RBF(sigma=1)
                KernelFunc.Poly(d=2, c=0)
        
        cut_value:
            the alpha result under cut_value will be assigned to 0.
            # alpha[alpha <= cut_value] = 0
 
            After cutting those small numbers, 
            the process of finding support vector(sv) could have more accuracy.
            
    output arg:
        predict_label: the predict result.
    """

    print('__svm_classfiy__')
    print(train_set, train_label, test_set, sep='\n')

    train_size = train_set.shape[0]
    x = train_set.to_numpy()
    y = train_label['G3'].to_numpy().astype(float)

    # Use HW8's data to test this model
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
    h = matrix(np.hstack((-np.zeros(train_size), C * np.ones(train_size))))

    # print(P, q, A, b, G, h)

    sv = solvers.qp(P, q, G, h, A, b)
    alpha = np.transpose(np.array(sv['x']))[0]

    alpha[alpha <= cut_value] = 0
    sv_index = np.where(alpha > cut_value)[0]
    print(alpha, sv_index, sep='\n')

    '''
    # we only need w in linear kernel, so I deleted it
    result_w = np.zeros(train_set.shape[1])
    for i in range(train_size):
        # print(result_alpha[i]*y[i]*x[i])
        result_w += alpha[i] * y[i] * x[i]
    print('w:', result_w)
    '''

    b = 0
    for i in sv_index:
        # print(i, y[i] - np.sum(result_w * x[i]))
        sum_val = 0
        for j in range(train_size):
            # Use specified kernel function
            sum_val += alpha[j] * y[j] * kernel.val(x[i], x[j])
        b += y[i] - sum_val
    b = b / len(sv_index)
    print('b:', b)

    # Plot (Only 2 Dimensions) (i.e. G1, G2):
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
        pred_val = 0
        for j in range(train_size):
            pred_val += alpha[j] * y[j] * kernel.val(x[j], test_data)
        pred_val += b
        predict_arr[i] = 1 if pred_val >= 0 else - 1
        
    predict_label = pd.Series(index=test_set.index,
                              data=predict_arr, name="predict")
    print(predict_label)
    return predict_label
