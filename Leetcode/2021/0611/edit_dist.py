def edit_dist(s, t):

    m, n = len(s), len(t)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):

            # 假设第一个字符串为空，则转换的代价为j（j次的插入）
            if i == 0:
                dp[i][j] = j
            # 假设第二个字符串为空，则转换的代价为i（i次的插入）
            elif j == 0:
                dp[i][j] = i
            elif s[i - 1] == t[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i][j - 1],  # insert
                    dp[i - 1][j],  # Remove
                    dp[i - 1][j - 1],  # Replace
                )
    return dp[-1][-1]


def common_substring_dp(s: str, t: str) -> int:
    m, n = len(s), len(t)
    table = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            table[i][j] = max(table[i - 1][j], table[i][j - 1],
                              int(s[i - 1] == t[j - 1]) + table[i - 1][j - 1])
    return table[-1][-1]


res = edit_dist('apple', 'appl')
print(res)