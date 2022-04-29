def constructArr(a):

    n = len(a)
    res = [1] * n

    for i in range(1, n):
        for num in a[:i]:
            res[i] *= num

    for i in range(n - 1):
        for num in a[i + 1:]:
            res[i] *= num
    return res


def constructArr2(a):
    b, tmp = [1] * len(a), 1
    for i in range(1, len(a)):
        b[i] = b[i - 1] * a[i - 1]  # 下三角
    for i in range(len(a) - 2, -1, -1):
        tmp *= a[i + 1]  # 上三角
        b[i] *= tmp  # 下三角 * 上三角
    return b


if __name__ == "__main__":
    a = [1, 2, 3, 4, 5]
    res = constructArr2(a)
    print(res)