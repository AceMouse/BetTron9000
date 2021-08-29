def _get_edit_distance(A, B):
    matrix = []
    for i in range(len(B)+1):
        matrix.append([i])
        if i == 0:
            for j in range(1, len(A)+1):
                matrix[i].append(j)

    for i in range(1, len(B)+1):
        for j in range(1, len(A)+1):
            matrix[i].append(min(matrix[i][j-1], matrix[i-1][j-1], matrix[i-1][j]))
            if B[i-1] != A[j-1]:
                matrix[i][j] += 1

    return matrix[-1][-1]


def is_similar(A, B):
    return _get_edit_distance(A, B) < ((len(A)+len(B))/2)*0.6





