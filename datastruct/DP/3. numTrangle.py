class Solution:
    def calMax(self, i, j):
        if i == self.n - 1:
            return self.D[i][j]
        x = self.calMax(i + 1, j)
        y = self.calMax(i + 1, j + 1)
        return max(x, y) + self.D[i][j]

    def maxSum(self, nums):
        self.n = len(nums[-1])
        self.D = [[0] * len(nums) for _ in range(self.n)]
        return self.calMax(0, 0)


if __name__ == "__main__":
    nums = [[7], [3, 8], [8, 1, 0], [2, 7, 4, 4], [4, 5, 2, 6, 5]]
    res = Solution()
    print(res.maxSum(nums))