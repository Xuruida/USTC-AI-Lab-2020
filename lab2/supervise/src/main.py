import KNN
import numpy as np
import pandas as pd
from pandas.api.types import is_string_dtype
from sklearn import preprocessing


def get_score(pred_label, test_label):
    if len(pred_label) != len(test_label):
        print("Length Error.")
        return (-1)

    TP, FN, FP, TN = 0, 0, 0, 0

    for i in range(len(pred_label)):
        if (pred_label[i] == 1):
            if (test_label[i] == 1):
                TP += 1
            else:
                FP += 1
        else:
            if (test_label[i] == 1):
                FN += 1
            else:
                TN += 1

    print("TP: %d, FP: %d, TN: %d, FN: %d" % (TP, FP, TN, FN))
    P_rate = TP / (TP + FP)
    R_rate = TP / (TP + FN)

    F1_score = (2 * P_rate * R_rate) / (P_rate + R_rate)
    print(F1_score)
    return F1_score

if __name__ == '__main__':
    # Read from csv file
    file = pd.read_csv('../data/student-mat.csv', delimiter=';')
    df = pd.DataFrame(file)
    print(df)

    # Transform into int
    for index in df.columns:
        # print('Column: ', index)
        if is_string_dtype(df[index]):  # is string
            col = df[index].to_numpy()
            le = preprocessing.LabelEncoder()
            fit_arr = np.unique(col)
            # print(fit_arr)
            # le.fit(fit_arr)
            # le.transform()
            # print(le.classes_)
            column_fit = le.fit_transform(df[index])
            # print(column_fit)
            df[index] = column_fit

    df['G3'] = df['G3'].apply(lambda x: 1 if x >= 10 else 0)
    print(df)

    seed_list = [10, 32, 63, 1024, 1621]

    # df.loc[:, ['G1', 'G2']] # Use G1, G2
    # df.drop('G3') # Use Attr without G3
    train_set = [df.loc[:, ['G1', 'G2']].sample(
        frac=0.7, random_state=x, axis=0).sort_index(axis=0) for x in seed_list]
    test_set = [df.loc[:, ['G1', 'G2']][~df.index.isin(
        train_set[x].index)] for x in range(len(seed_list))]
    train_label = [df.loc[:, ['G3']].sample(
        frac=0.7, random_state=x, axis=0).sort_index(axis=0) for x in seed_list]
    test_label = [df.loc[:, 'G3'][~df.index.isin(
        train_set[x].index)] for x in range(len(seed_list))]

    predict_label = []
    score_list = np.zeros(len(seed_list))
    for i in range(len(seed_list)):
        print("\niteration: ", i)
        predict_label.append(KNN.knn_classify(train_set[i], train_label[i], test_set[i], 9))
        print(test_label[i])
        score_list[i] = get_score(predict_label[i].to_numpy(), test_label[i].to_numpy())
    print(score_list)