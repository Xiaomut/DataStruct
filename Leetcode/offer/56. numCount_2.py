def singleNumbers(nums):
    count = [0] * 32

    for num in nums:
        for i in range(32):
            count[i] += num & 1
            num >>= 1

    res = 0
    for i in range(32):
        res <<= 1
        res |= count[31 - i] % 3

    if count[31] % 3 == 0:
        return res
    return ~(res ^ 0xffffffff)


if __name__ == "__main__":
    nums = [9, 1, 7, 9, 7, 9, 7]
    res = singleNumbers(nums)
    print(res)
