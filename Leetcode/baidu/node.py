# T = int(input())
# for _ in range(T):
#     n = int(input())
#     nums = [int(i) for i in input().split()]

import math

# nums = int(input())

# for _ in nums:

#     num = int(input())

num = 2
l, r = 1, math.floor(math.pow(num, 1 / 3))
flag = False

while l <= r:
    if math.pow(l, 3) + math.pow(r, 3) < num:
        l += 1
    elif math.pow(l, 3) + math.pow(r, 3) > num:
        r -= 1
    else:
        flag = True
        print("Yes")
        break
if not flag:
    print("No")