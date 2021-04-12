"""
Example 1:

Input: 
nums = 
[[1,2],
 [3,4]]

r = 1, c = 4

Output: 
[[1,2,3,4]]

Example 2:

Input: 
nums = 
[[1,2],
 [3,4]]

r = 2, c = 4

Output: 
[[1,2],
 [3,4]]
"""


def matrixReshape(nums, r, c):
    res = [[]]
    for i in nums:
        res[0] += i
    if r * c != len(res[0]):
        return nums
    out = [[] for _ in range(r)]
    num = 0
    count = 0
    for i in res[0]:
        if (num + 1) % c != 0:
            out[count].append(i)
        else:
            out[count].append(i)
            count += 1
        num += 1
    return out


print(matrixReshape(nums=[[1, 2], [3, 4], [3, 3]], r=3, c=2))
"""
Runtime: 96 ms, faster than 77.71% of Python3 online submissions for Reshape the Matrix.
Memory Usage: 15.3 MB, less than 48.72% of Python3 online submissions for Reshape the Matrix.
"""