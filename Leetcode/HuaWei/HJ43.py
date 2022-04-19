m, n = map(int, input().split())
grid = [0] * n
for i in range(m):
    x = [int(i) for i in input().split()]
    grid[i] = x

res = []


def dfs(grid, i, j, path):
    if i == m - 1 and j == n - 1:
        for t in path:
            print(t)

    for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        if 0 <= dx + i < m and 0 <= dy + j < n and grid[i][j] == 0:
            grid[i][j] = 1
            dfs(grid, dx + i, dy + j, path + [(dx + i, dy + j)])
            grid[i][j] = 0


dfs(grid, 0, 0, res)
