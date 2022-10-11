import math

N, X, Y = 6, 3, 1
# N, X, Y = map(int, input().split(','))
already = 0
n = 0
while already < N:
    n += 5
    already += X
    if already < N:
        already -= Y
n -= (already - N) / 5 * X
print(math.floor(n))
