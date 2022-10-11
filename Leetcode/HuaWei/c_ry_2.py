n = int(input())
grid = []
for _ in range(n):
    grid.append(list(input()))
print(grid)

if len(grid) == 0 or len(grid[0]) == 0:
    print(0)

res = 0
rows, columns = len(grid), len(grid[0])
dp = [[0] * columns for _ in range(rows)]
for i in range(rows):
    for j in range(columns):
        if grid[i][j] == '1':
            if i == 0 or j == 0:
                dp[i][j] = 1
            else:
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1],
                               dp[i - 1][j - 1]) + 1
            res = max(res, dp[i][j])

print(res**2)
