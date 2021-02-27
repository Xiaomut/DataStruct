'''
@File    :   _209_minSubArrayLen.py
@Time    :   2021/02/03 10:05:11
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''


def minSubArrayLen(s, nums):
    length = len(nums)
    if length == 1:
        if nums[0] >= s:
            return 1
        else:
            return 0

    vals_num = 0
    for index, num in enumerate(nums[:-1]):
        val = num
        save_len = 1
        if val >= s:
            return 1
        for sub_num in nums[index + 1:]:
            val += sub_num
            save_len += 1
            if val >= s:
                if vals_num == 0:
                    vals_num = save_len
                else:
                    vals_num = min(vals_num, save_len)
                break
    return vals_num


# print(minSubArrayLen(s=7, nums=[2, 3, 1, 2, 4, 3]))


def minSubArrayLen(s: int, nums) -> int:
    l = r = 0
    start = 0
    end = len(nums) - 1
    total = 0
    while r < len(nums):

        if total + nums[r] < s:
            total += nums[r]
            r += 1
        else:
            if r - l + 1 < end - start + 1:
                start = l
                end = r
            total -= nums[l]
            l += 1

    total = sum(nums[start:end + 1])
    if total >= s:
        return end - start + 1
    return 0