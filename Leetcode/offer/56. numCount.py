def singleNumbers(nums):
    x, y, n, m = 0, 0, 0, 1
    for num in nums:  # 1. 遍历异或
        n ^= num
    while n & m == 0:  # 2. 循环左移，计算 m
        m <<= 1
    for num in nums:  # 3. 遍历 nums 分组
        if num & m:
            x ^= num  # 4. 当 num & m != 0
        else:
            y ^= num  # 4. 当 num & m == 0
    return x, y  # 5. 返回出现一次的数字


if __name__ == "__main__":
    res = singleNumbers(nums=[5, 1, 2, 3, 1, 2])
    print(res)
