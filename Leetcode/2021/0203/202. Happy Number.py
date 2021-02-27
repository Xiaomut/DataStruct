'''
@File    :   202. Happy Number.py
@Time    :   2021/02/03 10:50:49
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''

# Time complexity: O(c)
# Space complexity: O(c)

# c = number of elements visited before cycle


class Solution:
    def isHappy(self, n):
        D = {
            n,
        }
        while True:
            n = sum(int(x)**2 for x in str(n))
            if n == 1:
                return True
            if n in D:
                return False
            D.add(n)


# Time complexity: O(c)*
# Space complexity: O(1)

# c = number of elements visited before cycle

# Note*: Floyd's Hare and Tortoise algorithm uses less memory, but it can actually take longer to run than a traditional HashSet implementation. (it still works with Linear Time Complexity though, it's just a bit slower due to the higher number of repeated operations)


class Solution2:
    def isHappy(self, n):
        move = lambda n: sum(int(x)**2 for x in str(n))
        slow, fast = n, n
        while True:
            slow = move(slow)
            fast = move(move(fast))
            if fast == 1:
                return True
            if fast == slow:
                return False
