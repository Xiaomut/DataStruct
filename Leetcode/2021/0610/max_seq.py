"""
A[j] = max{ A[j - 1] + arr[j], arr[j]}
"""


def max_subseq(arr):
    max_num = 0
    res = -100

    for i in range(len(arr)):
        if max_num + arr[i] >= arr[i]:
            max_num = max_num + arr[i]
        else:
            max_num = arr[i]

        res = max(res, max_num)
    return res


if __name__ == "__main__":
    arr = [-2, -3, 4, -1, -2, 1, 5, -3]
    print(max_subseq(arr))
