"""
Given a non-empty 2D array grid of 0's and 1's, an island is a group of 1's 
(representing land) connected 4-directionally (horizontal or vertical.) 
You may assume all four edges of the grid are surrounded by water.
Find the maximum area of an island in the given 2D array. 
(If there is no island, the maximum area is 0.)
"""


class Solution:
    def maxAreaOfIsland(self, grid):
        res = 0
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                if grid[r][c] == 1:
                    a = self.area(grid, r, c)
                    res = max(res, a)
        return res

    def area(self, grid, r: int, c: int) -> int:
        if not self.inArea(grid, r, c):
            return 0
        if grid[r][c] != 1:
            return 0
        grid[r][c] = 2

        return 1 \
            + self.area(grid, r - 1, c) \
            + self.area(grid, r + 1, c) \
            + self.area(grid, r, c - 1) \
            + self.area(grid, r, c + 1)

    def inArea(self, grid, r: int, c: int) -> bool:
        return 0 <= r < len(grid) and 0 <= c < len(grid[0])