'''
@File    :   4. quicksort.py
@Time    :   2022/01/26 19:26:24
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''
import random


class Solution:
    def randomized_partition(self, nums, l, r):
        # pivot = random.randint(l, r)
        pivot = 0
        nums[pivot], nums[r] = nums[r], nums[pivot]
        i = l - 1
        for j in range(l, r):
            if nums[j] < nums[r]:
                i += 1
                nums[j], nums[i] = nums[i], nums[j]
        i += 1
        nums[i], nums[r] = nums[r], nums[i]
        return i

    def randomized_quicksort(self, nums, l, r):
        if r <= l:
            return
        mid = self.randomized_partition(nums, l, r)
        self.randomized_quicksort(nums, l, mid - 1)
        self.randomized_quicksort(nums, mid + 1, r)

    def sortArray(self, nums):
        self.randomized_quicksort(nums, 0, len(nums) - 1)
        return nums


if __name__ == "__main__":
    solution = Solution()
    nums = [21, 88, 19, 45, 13, 25, 66, 33, 18]
    res = solution.sortArray(nums)