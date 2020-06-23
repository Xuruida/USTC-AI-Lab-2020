import numpy as np

def PCA(data: np.array, threshold: float):
    
    print("================", "Start PCA:", "================", sep='\n')
    print("Original Data:", data, sep='\n')
    n = data.shape[0]
    S_matrix = np.dot(data.transpose(), data) / n
    print("S:", S_matrix, sep='\n')

    eig_tuple = np.linalg.eig(S_matrix)
    print('eigenvalues and eigenvectors:\n', eig_tuple)
    sum_eigval = np.sum(eig_tuple[0])

    # Select first m eigenvalues
    sum_now = 0
    for m in range(len(eig_tuple[0])):
        sum_now += eig_tuple[0][m]
        if sum_now / sum_eigval > threshold:
            m -= 1
            break

    if m < 0:
        m = 0

    print("m:", m)
    P_matrix = eig_tuple[1][:m]
    print("P:", P_matrix.transpose(), sep='\n')

    new_data = np.dot(P_matrix, data.transpose()).transpose()
    print("\nNew data with %d dimension(s):" % m, new_data, sep='\n')
    return new_data