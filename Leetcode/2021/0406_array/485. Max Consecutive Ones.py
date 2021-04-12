"""
Given a binary array, find the maximum number of consecutive 1s in this array.

Example 1:
Input: [1,1,0,1,1,1]
Output: 3
Explanation: The first two digits or the last three digits are consecutive 1s.
    The maximum number of consecutive 1s is 3.
"""


def findMaxConsecutiveOnes(nums):
    count = 0
    cur = 0
    for i in nums:
        if i == 0:
            cur = 0
        else:
            cur += 1
        count = max(count, cur)
    return count


"""
Runtime: 364 ms, faster than 37.28% of Python3 online submissions for Max Consecutive Ones.
Memory Usage: 14.5 MB, less than 18.52% of Python3 online submissions for Max Consecutive Ones.
"""