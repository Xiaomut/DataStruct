#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   maxRotateFunction.py
@Time    :   2020/11/08 21:52:18
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''


def maxRotateFunction(A):
    length = len(A)
    if length >= 10000:
        return
    indexs = list(range(length))
    max_num = sum([i*A[i] for i in indexs])
    for i in range(1, length):
        tmp_list = indexs[i:] + indexs[:i]
        max_num = max(max_num, sum([tmp_list[j]*A[j] for j in indexs]))
    return max_num

"""
Every number except the last one will be added again (+s-A[n-1-i])
The current last number * (n-1) will be reduced from cur_sum
    A[n-1-i] * (n-1)
thus, cur_sum = cur_sum + s - A[n-1-i] - A[n-1-i] * (n-1) = cur_sum + s - A[n-1-i] * n
Iterate n times and return the maximum
Time complexity:
O(n) to initialize
O(n) to try all rotations
Total: O(2n) -> O(n)
"""
def maxRotateFunction(A):
    s, n = sum(A), len(A)
    cur_sum = sum([i*j for i, j in enumerate(A)])
    ans = cur_sum
    for i in range(n): ans = max(ans, cur_sum := cur_sum + s-A[n-1-i]*n)
    return ans


# F(i) = F(i-1) + sum(A) - A[-i]
def maxRotateFunction(A):
    ans = val = sum(i*x for i, x in enumerate(A))
    ss = sum(A)
    for x in reversed(A):
        val += ss - len(A)*x
        ans = max(ans, val)
    return ans 


A = [1]
# print(len(A))
print(maxRotateFunction(A))
