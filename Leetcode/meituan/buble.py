# n = int(input())
# nums = [int(i) for i in input().split()]

n = 4
nums = [3, -3, 1, -4, 2, -2, -1, 4]
res = 0
for i in range(1, len(nums)):
    # flag = True
    for j in range(1, len(nums) - i):
        if (int(nums[j]) > int(nums[j + 1])):
            nums[j], nums[j + 1] = nums[j + 1], nums[j]
            res += 1
    #         flag = False
    # if flag:
    #     break
print(res)
