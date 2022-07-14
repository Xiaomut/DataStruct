def nextGreaterElement(nums1, nums2):
    res = {}
    stack = []
    # 反向遍历
    for num in reversed(nums2):
        while stack and num >= stack[-1]:
            stack.pop()
        res[num] = stack[-1] if stack else -1
        stack.append(num)
    return [res[num] for num in nums1]


def nextGreaterElements(nums):
    n = len(nums)
    ret = [-1] * n
    stk = list()

    # 正向遍历
    for i in range(n * 2 - 1):
        # 索引用余数
        while stk and nums[stk[-1]] < nums[i % n]:
            ret[stk.pop()] = nums[i % n]
        stk.append(i % n)

    return ret


if __name__ == "__main__":
    nums1 = [4, 1, 2]
    nums2 = [1, 3, 4, 2]
    nums = [1, 2, 3, 4, 3]
    res = nextGreaterElement(nums1, nums2)
    res = nextGreaterElements(nums)
    print(res)
