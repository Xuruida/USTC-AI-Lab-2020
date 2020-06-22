import numpy as np
import pandas as pd
from pandas.api.types import is_string_dtype
from sklearn import preprocessing

import sys
import getopt


def get_score(pred_label, test_label):
    if len(pred_label) != len(test_label):
        print("Length Error.")
        return (-1)

    print(pred_label, test_label, sep='\n')

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
    use_knn, use_svm, use_dt = False, False, False
    if not sys.argv[1:]:
        use_knn, use_svm, use_dt = True, True, True
    elif sys.argv[1] in ("knn", "k"):
        use_knn = True
    elif sys.argv[1] in ("svm", "s"):
        use_svm = True
    elif sys.argv[1] in ("dt", "d"):
        use_dt = True
    else:
        print("Invalid Args: Arg not in ('knn', 'svm', 'dt', 'k', 's', 'd')")
        sys.exit(2)
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

    df['G3'] = df['G3'].apply(lambda x: 1 if x >= 10 else -1)
    print(df)

    seed_list = [10, 32, 63, 1024, 1621]

    # Use sample to get train and test sets.
    # df.loc[:, ['G1', 'G2']] # Use G1, G2
    # df.drop('G3') # Use Attr without G3
    train_set = [df.drop(['G3'], axis=1).sample(
        frac=0.7, random_state=x, axis=0).sort_index(axis=0) for x in seed_list]
    test_set = [df.drop(['G3'], axis=1)[~df.index.isin(
        train_set[x].index)] for x in range(len(seed_list))]
    train_label = [df.loc[:, ['G3']].sample(
        frac=0.7, random_state=x, axis=0).sort_index(axis=0) for x in seed_list]
    test_label = [df.loc[:, 'G3'][~df.index.isin(
        train_set[x].index)] for x in range(len(seed_list))]

    # KNN Classify
    if use_knn:

        KNN_predict_label = []
        KNN_score_list = np.zeros(len(seed_list))

        import KNN
        K = 9
        for i in range(len(seed_list)):
            print("\niteration: ", i)
            print("train_set %d:" % i, train_set[i], "train_label %d:" %
                  i, train_label[i], "test_set %d:" % i, test_set[i], sep='\n')
            KNN_predict_label.append(KNN.knn_classify(
                train_set[i], train_label[i], test_set[i], K))
            print(test_label[i])
            KNN_score_list[i] = get_score(
                KNN_predict_label[i].to_numpy(), test_label[i].to_numpy())
        print(KNN_score_list)
    
    # SVM Classify
    if use_svm:

        SVM_predict_label = []
        SVM_score_list = np.zeros(len(seed_list))

        import SVM
        ker = SVM.KernelFunc.RBF(30)  # Specify Kernel: Linear, RBF
        C = 10
        for i in range(len(seed_list)):
            print("\niteration: ", i)
            SVM_predict_label.append(SVM.svm_classify(
                train_set[i], train_label[i], test_set[i], C, kernel=ker, cut_value=1e-5))
            SVM_score_list[i] = get_score(
                SVM_predict_label[i].to_numpy(), test_label[i].to_numpy())

    if use_dt:
        
        DT_predict_label = []
        DT_score_list = np.zeros(len(seed_list))
        import other
        for i in range(len(seed_list)):
            print("\niteration: ", i)
            DT_predict_label.append(other.dt_classify(train_set[i], train_label[i], test_set[i]))
            DT_score_list[i] = get_score(DT_predict_label[i].to_numpy(), test_label[i].to_numpy())

    print("==========\nResult:\n==========\n")
    if use_knn:
        print("----------\nKNN: \n\nK: %d" % K,
              "\nScore_list:", KNN_score_list,
              "\nAverage Score:", np.mean(KNN_score_list))

    if use_svm:
        print("----------\nSVM: \n\nC: %f\n" % C,
              "Kernel Type: %s" % ker.name,
              "\nScore_list:", SVM_score_list,
              "\nAverage Score:", np.mean(SVM_score_list))

    if use_dt:
        print("----------\nDT: \n",
              "\nScore_list:", DT_score_list,
              "\nAverage Score:", np.mean(DT_score_list))
