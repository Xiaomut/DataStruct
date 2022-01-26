def threeSum(nums):
    n = len(nums)
    if n < 3:
        return []
    
    nums = sorted(nums)
    res = []
    for i in range(n-2):
        l, r = i + 1, n - 1
        if i >= 1 and nums[i] == nums[i-1]:
            continue
        while l < r:
            if l > i+1 and nums[l] == nums[l-1]:
                l += 1
                continue
            print(nums[i], nums[l], nums[r])
            sums = nums[i] + nums[l] + nums[r]
            if sums == 0:
                # if [nums[i], nums[l], nums[r]] not in res:
                res.append([nums[i], nums[l], nums[r]])
                l += 1
                r = n - 1
            elif sums > 0:
                r -= 1
            else:
                l += 1
    return res


if __name__ == "__main__":
    nums = [-1,0,1,2,-1,-4]
    res = threeSum(nums)
    print(res)