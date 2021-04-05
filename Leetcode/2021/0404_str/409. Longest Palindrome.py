"""
409. Longest Palindrome

Given a string s which consists of lowercase or uppercase letters, return the length of the longest palindrome that can be built with those letters.
Letters are case sensitive, for example, "Aa" is not considered a palindrome here.


Example 1:

Input: s = "abccccdd"
Output: 7
Explanation:
One longest palindrome that can be built is "dccaccd", whose length is 7.
Example 2:

Input: s = "a"
Output: 1
Example 3:

Input: s = "bb"
Output: 2

"""
from collections import Counter


def longestPalindrome(s: str) -> int:
    s_count = dict(Counter(s))
    print(s_count)
    num = 0
    flag = False
    for i in s_count.values():
        # if i > 1:
        if i % 2 == 0:
            num += i
        else:
            flag = True
            num += (i - 1)

    if flag:
        num += 1
    return num


print(longestPalindrome(s="aaa"))
"""
Runtime: 28 ms, faster than 90.47% of Python3 online submissions for Longest Palindrome.
Memory Usage: 14.3 MB, less than 57.22% of Python3 online submissions for Longest Palindrome.
"""