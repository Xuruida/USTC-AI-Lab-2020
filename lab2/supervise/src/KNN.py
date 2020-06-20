import numpy as np
import pandas as pd
import math

import time

# calculate distance


def calc_dis(a: np.array, b: np.array):
    """
    Calculate Euclidian Distance of two data.
    Return distance.
    """
    sum = 0
    for i in range(len(a)):
        sum = sum + (a[i] - b[i]) * (a[i] - b[i])
    result = math.sqrt(sum)
    return result

# KNN
def knn_classify(train_set: pd.DataFrame, train_label: pd.DataFrame, test_set: pd.DataFrame, k_value: int):
    """
    KNN Classify 'G3' in train_label
    """

    start_t = time.clock()

    print(train_set.shape[0], test_set.shape[0], "\n")

    # initialize
    predict_arr = np.zeros(test_set.shape[0], dtype=int)
    distance_arr = np.zeros(train_set.shape[0], dtype=float)

    # Transform DataFrame to NumPy
    train_set_arr = train_set.to_numpy()
    train_label_arr = train_label['G3'].to_numpy()
    # print(train_label_arr)
    test_set_arr = test_set.to_numpy()

    for i, test_data in enumerate(test_set_arr):
        # print(i, test_data)

        for j, train_data in enumerate(train_set_arr):
            distance_arr[j] = calc_dis(test_data, train_data)

        dis_rank = np.argsort(distance_arr)
        
        nearest_label_arr = train_label_arr[dis_rank[:k_value]]

        #print(dis_rank[:k_value],
        #      distance_arr[dis_rank[:k_value]],
        #      nearest_label_arr,
        #      sep='\n'
        #      )
        pass_cnt = 0
        for item in nearest_label_arr:
            if item == 1:
                pass_cnt = pass_cnt + 1
        # print(pass_cnt)
        if pass_cnt >= k_value - pass_cnt:
            predict_arr[i] = 1
        else:
            predict_arr[i] = 0

    print(predict_arr)
    predict_label = pd.Series(data=predict_arr, index=test_set.index, name="predict")
    print(predict_label)
    return predict_label