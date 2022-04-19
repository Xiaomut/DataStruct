s1 = "abcdefghijklmnop"
s2 = "abcsafjklmnopqrstuvw"
if len(s1) > len(s2):
    s1, s2 = s2, s1
n1, n2 = len(s1), len(s2)
dp = [[0] * (n2) for _ in range(n1)]

index = 0
max_num = 0
for i in range(1, n1):
    for j in range(1, n2):
        if s1[i] == s2[j]:
            dp[i][j] = dp[i - 1][j - 1] + 1
            if dp[i][j] > max_num:
                max_num = dp[i][j]
                index = i
        else:
            dp[i][j] = 0
print(s1[index - max_num+1:index+1])
