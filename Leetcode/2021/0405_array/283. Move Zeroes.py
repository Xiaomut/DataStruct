"""
Given an integer array nums, move all 0's to the end of it while maintaining the relative order of the non-zero elements.
Note that you must do this in-place without making a copy of the array.

Example 1:

Input: nums = [0,1,0,3,12]
Output: [1,3,12,0,0]
Example 2:

Input: nums = [0]
Output: [0]
 
"""


def moveZeroes(nums) -> None:
    """
    Do not return anything, modify nums in-place instead.
    """
    length = len(nums)
    i = 0
    count_num = 0
    while count_num < length:
        count_num += 1
        if nums[i] == 0:
            nums.remove(nums[i])
            nums.append(0)
        else:
            i += 1
    return nums


print(moveZeroes([0, 0, 1, 0]))
"""
Runtime: 84 ms, faster than 22.26% of Python3 online submissions for Move Zeroes.
Memory Usage: 15.4 MB, less than 18.80% of Python3 online submissions for Move Zeroes.
"""