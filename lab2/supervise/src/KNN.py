import numpy as np
import pandas as pd
import math

import time

# calculate distance
def calc_dis(a: list, b: list):
    """
    Calculate Euclid Distance of two data.
    Return distance.
    """
    sum = 0
    for i in range(len(a)):
        sum = sum + (a[i] - b[i]) * (a[i] - b[i])
    result = math.sqrt(sum)
    return result

# KNN
def knn_fit(train_set: pd.DataFrame, test_set: pd.DataFrame, k_value: int):
    """
    Use kNN method to predict G3.
    Return Score.
    """

    start_t = time.clock()

    print(train_set.shape[0], test_set.shape[0])
    predict_list = pd.DataFrame(index=test_set.index, data=test_set['G3'])
    dis_list = pd.DataFrame(index=train_set.index, columns=['G3'], data=train_set['G3'])
    print(predict_list)
    test_set = test_set.drop('G3', axis=1)

    train_set_dropped_G3 = train_set.drop('G3', axis=1)
    
    for i, test_row in test_set.iterrows():
        print(i, test_row.values)
        # t1 = time.clock()
        for j, train_row in train_set_dropped_G3.iterrows():
            distance = calc_dis(test_row.to_list(),
                train_row.to_list())
            dis_list.loc[j, 'distance'] = distance
        # t2 = time.clock()
        # print('TIME: %f', t2 - t1)
        dis_list = dis_list.sort_values(by='distance', ascending=True)
        # print(dis_list.iloc[:k_value])
        pass_cnt = 0
        for j in range(k_value):
            if (dis_list.iloc[j].loc['G3'] >= 10):
                pass_cnt += 1
        if (pass_cnt >= k_value - pass_cnt):
            predict_list.loc[i, 'pred'] = 'P' # Pass
        else:
            predict_list.loc[i, 'pred'] = 'F' # Fail
        # print(i, pass_cnt, '\n', dis_list.iloc[:k_value])

    print(predict_list)

    TP, FP, TN, FN = 0, 0, 0, 0
    for i in predict_list.index:
        pred_row = predict_list.loc[i]
        if (pred_row['G3'] >= 10):
            if (pred_row.pred == 'P'):
                TP += 1
            else:
                FN += 1
        else:
            if (pred_row.pred == 'P'):
                FP += 1
            else:
                TN += 1
    
    print('TP: %d; FP: %d; TN: %d; FN: %d.' % (TP, FP, TN, FN))

    P_rate = TP / (TP + FP)
    R_rate = TP / (TP + FN)
    F1_score = (2 * P_rate * R_rate) / (P_rate + R_rate)

    print('F1 Score: %f' % F1_score)

    stop_t = time.clock()
    print('time: ', stop_t - start_t)
    
    res_dict = {
        'F1_score': F1_score,
        'pred_result': predict_list
    }

    return res_dict
