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
    for i in range(train_set.shape[0]): # Normalize with mean # and standard deviation
        train_set[i] = (train_set[i] - mean) / s
    print(train_set) 
    print(np.mean(train_set, axis=0), np.var(train_set, axis=0), sep='\n')

    train_set_PCA = PCA(train_set, 0.99)

    # plot_3D(train_set_PCA, label_set)

    cluster_label = kmeans.kmeans_cluster(3, train_set_PCA)

    plot_2D_2(train_set_PCA, label_set, cluster_label)