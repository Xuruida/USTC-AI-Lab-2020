import numpy as np

def get_euclidean_dis(a: np.array, b: np.array):
    return np.sqrt(np.sum((a - b) ** 2))

def kmeans_cluster(k: int, data: np.array):
    """
    K-Means Cluster.
    """
    print("================\n")
    print("Start K-Means:\n================\n", "K: %d" % k, sep = '\n')

    n = data.shape[0]

    # Initialize K-Means with k-means++ algo.
    first_centroid_idx= np.random.randint(n)
    centroids = [data[first_centroid_idx]]
    print(centroids)
    for i in range(1, k):
        distances = np.zeros(n, dtype=float)
        for j in range(n):
            min_dis = -1
            for centroid in centroids:
                distance = np.sum((np.array(centroid) - data[j]) ** 2)
                if min_dis < 0 or min_dis > distance:
                    min_dis = distance
            distances[j] = min_dis
        sum_dis = np.sum(distances)
        p = distances / sum_dis
        next_centroid_idx = np.random.choice(n, p=p)
        print(next_centroid_idx)
        centroids.append(data[next_centroid_idx])

    centroids = np.array(centroids)
    print(centroids)

    cluster_label = np.zeros(n, dtype=int)
    # Cluster Change
    cluster_changed = True
    iter_num = 0
    while cluster_changed:
        print("iteration: %d" % iter_num)
        iter_num = iter_num + 1
        cluster_changed = False

        # Update cluster of each data
        for i, row_data in enumerate(data):
            distances = np.zeros(k, dtype=float)
            for j, centroid in enumerate(centroids):
                distances[j] = get_euclidean_dis(centroid, row_data)
            # print(i, distances, sep='\n')
            new_idx = np.argmin(distances)
            if new_idx != cluster_label[i]:
                cluster_label[i] = new_idx
        print(cluster_label)

        # Update Cluster
        for i in range(k):
            data_in_i = data[cluster_label == i]
            centroid_new = np.mean(data_in_i, axis=0)
            print(centroid_new)
            if (centroid_new != centroids[i]).all():
                cluster_changed = True
                centroids[i] = centroid_new
        print(centroids)
    
    return cluster_label