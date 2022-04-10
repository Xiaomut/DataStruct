def spiralOrder(matrix):
    res = []
    while matrix:
        res += matrix.pop(0)
        mtxzip = zip(*matrix)
        tmp = list(mtxzip)
        matrix = tmp[::-1]
    return res


def spiralOrder2(matrix):
    res = []
    if matrix == []:
        return res

    top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1

    while left <= right and top <= bottom:
        for i in range(left, right + 1):
            res.append(matrix[top][i])
        top += 1

        for i in range(top, bottom + 1):
            res.append(matrix[i][right])
        right -= 1

        if left > right or top > bottom:
            break

        for i in range(right, left - 1, -1):
            res.append(matrix[bottom][i])
        bottom -= 1

        for i in range(bottom, top - 1, -1):
            res.append(matrix[i][left])
        left += 1

    return res


if __name__ == "__main__":
    # matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    # res = spiralOrder2(matrix)
    print(len([[]]))