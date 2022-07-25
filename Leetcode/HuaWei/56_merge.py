def merge(intervals):

    if len(intervals) <= 1:
        return intervals

    nums1 = [i[0] for i in intervals][1:]
    nums2 = [i[1] for i in intervals][:-1]

    res1, res2 = [intervals[0][0]], []
    flag = False
    for idx, (prev, post) in enumerate(zip(nums1, nums2)):
        if post >= prev:
            if flag:
                res2.pop()
            res2.append(intervals[idx + 1][1])
            flag = True
        else:
            res1.append(intervals[idx + 1][0])
            res2.append(intervals[idx + 1][1])
            flag = False
    print(res1)
    print(res2)
    return [[i, j] for (i, j) in zip(res1, res2)]


if __name__ == "__main__":
    intervals = [[1, 4], [5, 6]]
    res = merge(intervals)
    print(res)