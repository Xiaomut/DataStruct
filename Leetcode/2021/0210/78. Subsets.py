def subsets(nums):
    def dfs(i, path):
        print(f"The i is {i}    The path is {path}")
        if i == len(nums):
            return res.append(path)
        print(f'----------1. 执行第一个dfs------------')
        dfs(i + 1, path + [nums[i]])
        print(f'nums[i] = {nums[i]}')
        print(f'----------2. 执行第二个dfs------------')
        dfs(i + 1, path)

    res = []
    dfs(0, [])
    return res


# 1.1 回溯法
class Solution:
    # N is the size of nums
    # Time Complexity: O(N*2^N)
    # Space Complexity: O(N*2^N)
    def subsets(self, nums):
        result = [[]]
        for i in range(1, len(nums) + 1):
            self.backtracking(nums, result, i, 0, [])
        return result

    def backtracking(self, nums, result, length, index, subset):
        if len(subset) == length:
            result.append(subset[:])
            return

        for i in range(index, len(nums)):
            subset.append(nums[i])
            self.backtracking(nums, result, length, i + 1, subset)
            subset.pop()


# 1.2 暴力法
def subsets2(nums):
    # Time Complexity: O(N*2^N)
    # Space Complexity: O(N*2^N)
    subset = [[]]
    for i in nums:
        for j in subset:
            subset = subset + [j + [i]]

    return subset


# 1.3 深度优先搜索法
class Solution:
    # Leetcode 78. SUbsets
    # Bilibili|公众号|Youtube: @爱学习的饲养员
    # DFS
    # N is the size of nums
    # Time Complexity: O(N*2^N)
    # Space Complexity: O(N*2^N)
    def subsets(self, nums):
        result = []
        self.dfs(nums, result, 0, [])
        return result

    def dfs(self, nums, result, index, subset):
        result.append(subset[:])
        if index == len(nums):
            return
        for i in range(index, len(nums)):
            subset.append(nums[i])
            self.dfs(nums, result, i + 1, subset)
            subset.pop()


print(subsets2(nums=[1, 2, 3]))
