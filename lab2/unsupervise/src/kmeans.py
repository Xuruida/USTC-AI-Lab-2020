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
    
    # Calculate Silhouette Coefficient
    sil_coef = np.zeros(n)

    if n != 1:
        for i in range(n):
            cluster_idx = cluster_label[i] # Find Cluster index
            # Calculate a(i)
            data_in_i = data[cluster_label == cluster_idx]
            distances = np.zeros(len(data_in_i))
            for j in range(len(distances)):
                distances[j] = get_euclidean_dis(data_in_i[j], data[i])
            # print('a', distances)
            a = np.sum(distances) / (len(data_in_i) - 1)
            
            # Calculate b(i)
            b_arr = np.zeros(k)
            for j in range(k):
                if cluster_idx == j:
                    continue
                data_in_j = data[cluster_label == j]
                distances_j = np.zeros(len(data_in_j))
                for l in range(len(distances_j)):
                    distances_j[l] = get_euclidean_dis(data[i], data_in_j[l])  # Distances to Cluster j
                b_arr[j] = np.sum(distances_j) / len(data_in_j)
                # print('dis %d' % j, distances_j)
            # print('b', b_arr)

            # Find the second minimal value (Distance to cluster_idx == 0)
            b_arr[np.argmin(b_arr)] = np.max(b_arr) # 
            b = np.min(b_arr)
            # print(i, a, b)
            sil_coef[i] = (b - a) / max(a, b)
            # print(sil_coef[i])

    else:
        sil_coef[0] = 0

    print('Silhouette Coefficient:', sil_coef, sep='\n')
    return sil_coef, cluster_label
