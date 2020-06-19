import numpy as np
import pandas as pd
from pandas.api.types import is_string_dtype
from sklearn import preprocessing

# Read from csv file
file = pd.read_csv('../data/student-mat.csv', delimiter=';')
df = pd.DataFrame(file)
print(df)

# Transform into int
for index in df.columns:
    print('Column: ', index)
    if is_string_dtype(df[index]):  # is string
        col = df[index].to_numpy()
        le = preprocessing.LabelEncoder()
        fit_arr = np.unique(col)
        # print(fit_arr)
        # le.fit(fit_arr)
        # le.transform()
        # print(le.classes_)
        column_fit = le.fit_transform(df[index])
        print(column_fit)
        df[index] = column_fit

print(df)

seed_list = [10, 32, 63, 1024, 1621]

train_list = [df.loc[:, ['G1', 'G2', 'G3']].sample(frac=0.7, random_state=x, axis=0).sort_index(axis=0) for x in seed_list]
test_list = [df.loc[:, ['G1', 'G2', 'G3']][~df.index.isin(
    train_list[x].index)] for x in range(len(seed_list))]

import KNN

knn_score = [.0, .0, .0, .0, .0]
for i in range(len(seed_list)):
    print('train %d:' % i, train_list[i], sep='\n')
    print('test %d:' % i, test_list[i], sep='\n')
    knn_result = KNN.knn_fit(train_list[i], test_list[i], 9)
    knn_score[i] = knn_result['F1_score']
    
print(knn_score)
