# import sys
# n = int(sys.stdin.readline().strip())
n = 2


res = 1
if n == 1:
    print(res) 
dp = [0] * (n + 1)
dp[0] = dp[1] = 1
for i in range(2, n + 1):
    dp[i] = dp[i - 2] + dp[i - 1]
res = dp[n]
for j in range(1, n):
    res += dp[j] * dp[n - j + 1]
print(res) 

