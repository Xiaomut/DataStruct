def numIslands(grid) -> int:
    def dfs(grid, i, j):
        if i < 0 or i >= len(grid) or j < 0 or j >= len(
                grid[0]) or grid[i][j] == '0':
            return False

        grid[i][j] = '0'
        dfs(grid, i - 1, j) or dfs(grid, i + 1, j) or dfs(
            grid, i, j - 1) or dfs(grid, i, j + 1)

    res = 0

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if dfs(grid, i, j):
                res += 1
    return res


if __name__ == "__main__":
    grid = [["1", "1", "1", "1", "0"], ["1", "1", "0", "1", "0"],
            ["1", "1", "0", "0", "0"], ["0", "0", "0", "0", "0"]]
    print(numIslands(grid))