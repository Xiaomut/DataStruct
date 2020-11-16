def isAnagram(s: str, t: str) -> bool:
    nums = {}
    nums2 = {}
    for i in s:
        nums[i] = nums.get(i, 0) + 1
        # if i in nums.keys():
        #     nums[i] += 1
        # else:
        #     nums[i] = 1
    # print(nums)
    for i in t:
        nums[i] = nums.get(i, 0) + 1
        # if i in nums.keys():
        #     nums[i] -= 1
        # else:
        #     return 'false'
    # print(nums)
    # for i in nums.values():
    #     if i!=0:
    #         return 'false'
    # return 'true'
    return nums == nums2


print(isAnagram("a", "b"))
