import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_3D(train_set_PCA: np.array, label_set):
    # 3D plot
    x1 = train_set_PCA[label_set == 1, 0]
    y1 = train_set_PCA[label_set == 1, 1]
    z1 = train_set_PCA[label_set == 1, 2]

    x2 = train_set_PCA[label_set == 2, 0]
    y2 = train_set_PCA[label_set == 2, 1]
    z2 = train_set_PCA[label_set == 2, 2]

    x3 = train_set_PCA[label_set == 3, 0]
    y3 = train_set_PCA[label_set == 3, 1]
    z3 = train_set_PCA[label_set == 3, 2]

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x1, y1, z1, c='aqua', label='1')
    ax.scatter(x2, y2, z2, c='violet', label='2')
    ax.scatter(x3, y3, z3, c='lightgreen', label='3')
    plt.show()


def plot_2D(train_set_PCA: np.array, label_set):
    # 2D plot
    plt.scatter(train_set_PCA[label_set == 1, 0],
                train_set_PCA[label_set == 1, 1],
                c='aqua',
                marker='o')
    plt.scatter(train_set_PCA[label_set == 2, 0],
                train_set_PCA[label_set == 2, 1],
                c='violet',
                marker='o')
    plt.scatter(train_set_PCA[label_set == 3, 0],
                train_set_PCA[label_set == 3, 1],
                c='lightgreen',
                marker='o')
    plt.show()

def plot_2D_2(train_set_PCA: np.array, label_set_1: np.array, label_set_2: np.array):

    plt.subplot(1, 2, 1)
    plt.scatter(train_set_PCA[label_set_1 == 1, 0],
                train_set_PCA[label_set_1 == 1, 1],
                c='aqua',
                marker='o')
    plt.scatter(train_set_PCA[label_set_1 == 2, 0],
                train_set_PCA[label_set_1 == 2, 1],
                c='violet',
                marker='o')
    plt.scatter(train_set_PCA[label_set_1 == 3, 0],
                train_set_PCA[label_set_1 == 3, 1],
                c='lightgreen',
                marker='o')
    plt.grid(True)
    plt.title('Original Classification')
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.subplot(1, 2, 2)
    plt.scatter(train_set_PCA[label_set_2 == 0, 0],
                train_set_PCA[label_set_2 == 0, 1],
                c='aqua',
                marker='o')
    plt.scatter(train_set_PCA[label_set_2 == 1, 0],
                train_set_PCA[label_set_2 == 1, 1],
                c='violet',
                marker='o')
    plt.scatter(train_set_PCA[label_set_2 == 2, 0],
                train_set_PCA[label_set_2 == 2, 1],
                c='lightgreen',
                marker='o')
    plt.scatter(train_set_PCA[label_set_2 == 3, 0],
                train_set_PCA[label_set_2 == 3, 1],
                c='yellow',
                marker='o')
    plt.grid(True)
    plt.title('K-means Cluster')
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.show()
