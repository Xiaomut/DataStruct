def coins_dp(values, target):
    # memo[i]表示target为i的时候，所需的最少硬币数
    memo = [0] * (target + 1)
    # 0元的时候为0个
    memo[0] = 0

    for i in range(1, target + 1):
        min_num = 999999
        # 对于values中的所有n
        # memo[i]为 min(memo[i-n1], memo[i-n2], ...) + 1
        for n in values:
            if i >= n:
                min_num = min(min_num, 1 + memo[i - n])
            else:  # values中的数值要从小到大排序
                break
        memo[i] = min_num
    # print(memo)
    return memo[-1]


if __name__ == "__main__":
    values = [1, 3, 5]
    target = 23
    print(coins_dp(values, target))
