def movingCount(m: int, n: int, k: int) -> int:
    def process(x):
        if x < 10:
            return x
        elif x == 100:
            return 1
        else:
            return x // 10 + x % 10

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    dp[1][1] = 1

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if i == 1 and j == 1:
                continue
            if (dp[i - 1][j] == 1 or dp[i][j - 1]
                    == 1) and process(i - 1) + process(j - 1) <= k:
                dp[i][j] = 1

    return sum([sum(i) for i in dp])


if __name__ == "__main__":
    res = movingCount(1, 2, 1)
    print(res)