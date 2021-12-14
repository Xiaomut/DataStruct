def FindGreatestSumOfSubArray(array):
    # write code here
    length = len(array)
    dp = list(range(length+1))
    dp[0] = 0
    sum_ = 0
    ret = array[0]
    temp_idx, temp_len = 0, 0
    max_idx, max_len = 0, 0
    for i in range(1, length+1):
        if array[i-1] > sum_+array[i-1]:
            sum_ = array[i-1]
            temp_idx = i-1
            temp_len = 1
        else:
            sum_ = sum_ + array[i-1]
            temp_len += 1
        if ret <= sum_:
            if ret == sum_:
                if max_len < temp_len:
                    max_len = temp_len
                    max_idx = temp_idx
            else:
                max_len = temp_len
                max_idx = temp_idx
            ret = sum_
    return array[max_idx:max_idx+max_len]


if __name__ == "__main__":
    array = [1, -2, 3, 10, -4, 7, 2, -5]
    res = FindGreatestSumOfSubArray(array)
    print(res)