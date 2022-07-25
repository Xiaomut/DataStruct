class Solution:
    def movingCount(self, m: int, n: int, k: int) -> int:
        res = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if self.process(i) + self.process(j) <= k:
                    res[i][j] = 1
                else:
                    break
        print(res)
        return self.sum_one(res)

    def process(self, x):
        if x < 10 or x == 100:
            return x
        else:
            return x // 10 + x % 10

    def sum_one(self, nums):
        res = 0
        flag = False
        i = j = 0
        for i in range(len(nums) - 1):
            for j in range(len(nums[0]) - 1):
                res += 1
                if nums[i + 1][j] == 0 and nums[i][j + 1] == 0:
                    break
                elif nums[i][j + 1] == 1:
                    res += 1
            if nums[i + 1][j] == 0 and nums[i][j + 1] == 0:
                break
            flag = True
        if flag:
            res += sum(nums[-1])
        return res


if __name__ == "__main__":
    solution = Solution()
    print(solution.movingCount(3, 1, 0))