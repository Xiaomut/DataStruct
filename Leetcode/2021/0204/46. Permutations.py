'''
@File    :   46. Permutations.py
@Time    :   2021/02/04 19:31:53
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''


def permute(nums):
    final = []

    def dfs(nums, path):
        if len(nums) == 0 and path not in final:
            final.append(path)
        for i in range(len(nums)):
            dfs(nums[:i] + nums[i + 1:], path + [nums[i]])

    dfs(nums, [])
    return final


print(permute(nums=[1, 2, 3]))
