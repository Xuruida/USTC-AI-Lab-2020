import numpy as np
import pandas as pd

from math import log2
import random

def calc_entropy(data_label: np.array):
    length = data_label.shape[0]
    values = list(set(data_label))
    p = np.zeros(len(values), dtype=int)
    for i, label in enumerate(values):
        p[i] = len(data_label[data_label == label])
    p = p / length
    # print(p, length)
    entropy = np.sum(-p * np.log2(p))
    # print(entropy)
    return entropy

def best_feature(data_set, data_label, valid_set):
    length = len(data_set)
    print(data_set, valid_set)
    base_entropy = calc_entropy(data_label)
    axis_best = None
    gain_best = 0
    for i in valid_set:
        # print("column:", i)
        column = data_set[:, i]
        values = list(set(column))
        # print(values)
        new_entropy = 0.
        for j, val in enumerate(values):
            index_list = np.where(column == val)[0]
            new_entropy += calc_entropy(data_label[index_list]) * len(index_list) / length
        print(new_entropy)
        gain = base_entropy - new_entropy
        if gain > gain_best:
            axis_best = i
            gain_best = gain
        print("Now: ", i, gain_best)
    print(axis_best, gain_best)
    return axis_best

def create_tree(data_set: np.array, data_label: np.array, valid_set: set):
    
    # return axis index
    if len(valid_set) == 1 or len(set(data_label)) == 1:
        return data_label[0]

    axis_best = best_feature(data_set, data_label, valid_set)
    tree = {axis_best: {}}
    valid_set.remove(axis_best)
    values = list(set(data_set[:, axis_best]))
    for val in values:
        index_list = np.where(data_set[:, axis_best] == val)[0]
        print(index_list)
        tree[axis_best][val] = create_tree(data_set[index_list], data_label[index_list], valid_set)
    return tree

def predict(test_data: np.array, decision_tree: dict):
    if type(decision_tree) is not dict:
        return decision_tree
    for key in decision_tree.keys():
        print(key)
        sub_tree = decision_tree[key]
        next_key = test_data[key]
        if next_key in sub_tree.keys():
            return predict(test_data, sub_tree[next_key])
        else:
            print("RANDOM!")
            return random.choice([1, -1])

def dt_classify(train_set: pd.DataFrame, train_label: pd.DataFrame, test_set: pd.DataFrame):
    
    print("\n__dt_calssify__:\n")
    train_set_arr = train_set.to_numpy()
    train_label_arr = train_label['G3'].to_numpy()
    print(train_label['G3'].value_counts())
    calc_entropy(train_label_arr)
    
    initial_set = set(range(train_set_arr.shape[1]))
    best_feature(train_set_arr, train_label_arr, initial_set)
    decision_tree = create_tree(train_set_arr, train_label_arr, initial_set)
    print(decision_tree)

    test_arr = test_set.to_numpy()
    predict_arr = np.zeros(test_set.shape[0], dtype=int)
    for i, test_data in enumerate(test_arr):
        predict_arr[i] = predict(test_data, decision_tree)
    print(predict_arr)
    predict_label = pd.Series(index=test_set.index,
                                  data=predict_arr, name="predict")
    print(predict_label)
    return predict_label
