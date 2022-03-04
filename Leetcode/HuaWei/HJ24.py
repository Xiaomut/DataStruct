import bisect
def inc_max(l):
    dp = [1]*len(l) # 初始化dp，最小递增子序列长度为1
    arr = [l[0]] # 创建数组
    for i in range(1,len(l)): # 从原序列第二个元素开始遍历
        if l[i] > arr[-1]:
            arr.append(l[i])
            dp[i] = len(arr)
        else:
            pos = bisect.bisect_left(arr, l[i]) # 用二分法找到arr中第一个比ele_i大（或相等）的元素的位置
            arr[pos] = l[i]
            dp[i] = pos+1
    return dp 

if __name__ == "__main__":
    nums = "186 186 150 200 160 130 197 200"
    s = list(map(int, nums.split()))
    left_s = inc_max(s)
    print(left_s)
