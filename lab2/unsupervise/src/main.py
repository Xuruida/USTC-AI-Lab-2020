import numpy as np
from PCA import PCA
import kmeans

from plots import plot_2D, plot_3D, plot_2D_2

if __name__ == '__main__':
    data_set = np.loadtxt("../input/wine.data", delimiter=',')

    # Processing the input data
    label_set = data_set[:, 0].astype(int)  # Get labels
    train_set = data_set[:, 1:]  # Get train set
    print(label_set, train_set, sep='\n')

    # Normalize data
    mean = np.mean(train_set, axis=0)
    s = np.var(train_set, axis=0) ** 0.5
    # Normalize with mean # and standard deviation
    for i in range(train_set.shape[0]):
        train_set[i] = (train_set[i] - mean) / s
    print(train_set)
    print(np.mean(train_set, axis=0), np.var(train_set, axis=0), sep='\n')

    threshold = 1
    train_set_PCA = PCA(train_set, threshold)

    # plot_3D(train_set_PCA, label_set)

    sil_coef, cluster_label = kmeans.kmeans_cluster(3, train_set_PCA)
    # print(sil_coef)
    sil_coef_mean = np.mean(sil_coef)

    # Calculate Rand Index
    a, d = 0, 0
    n = len(label_set)
    for i in range(n):
        for j in range(i+1, n):
            if (label_set[i] == label_set[j]) and (cluster_label[i] == cluster_label[j]):
                a += 1
            elif (label_set[i] != label_set[j]) and (cluster_label[i] != cluster_label[j]):
                d += 1
    pair_cnt = n * (n - 1) // 2
    # print(a, d, pair_cnt)
    rand_index = (a + d) / pair_cnt

    # Print Result Information
    print("Original Classification:", label_set, sep='\n')
    print("K-means Cluster Result:", cluster_label, sep='\n')
    print("PCA:", "\tThreshold: %f" % threshold,
          "\tDimension(s) After PCA: %d" % train_set_PCA.shape[1], sep='\n')
    print("Silhouette Coefficient: %lf" % sil_coef_mean)
    print("Rand Index: %lf" % rand_index)
    plot_2D_2(train_set_PCA, label_set, cluster_label)
