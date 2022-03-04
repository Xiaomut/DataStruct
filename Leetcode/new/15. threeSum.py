class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:

        ans = []
        n = len(nums)
        nums.sort()  # 排序
        for i in range(n):
            left = i + 1
            right = n - 1

            if nums[i] > 0: break

            # 去重复逻辑：避免nums[i]重复
            if i >= 1 and nums[i] == nums[i - 1]:
                continue

            while left < right:
                total = nums[i] + nums[left] + nums[right]
                if total > 0:
                    right -= 1
                elif total < 0:
                    left += 1
                else:
                    ans.append([nums[i], nums[left], nums[right]])

                    # 去重复逻辑：避免nums[left]和humes[right]重复
                    while left != right and nums[left] == nums[left + 1]:
                        left += 1
                    while left != right and nums[right] == nums[right - 1]:
                        right -= 1

                    left += 1
                    right -= 1
        return ans


if __name__ == "__main__":
    pass