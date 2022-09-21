n = int(input())
nums = [int(i) for i in input().split()]
# nums = [7, 3, 11, 5, 2]
min_num = min(nums)
max_num = max(nums)

tenp_num = sorted(nums)[len(nums) // 2]
count = 0
for i, j in zip(
        nums,
        list(range(tenp_num - len(nums) // 2, tenp_num + len(nums) // 2 + 1))):
    if i != j:
        count += 1

nums = list(set(nums))
r = 1
ans = n
nums.sort()
for i in range(len(nums)):
    while r < len(nums) and (nums[r] - nums[i]) <= (n - 1):
        r += 1
    now = n - (r - i)
    if ans > now:
        ans = now

print(ans + count)
