"""
Given a string, your task is to count how many palindromic substrings in this string.
The substrings with different start indexes or end indexes are counted as different substrings even they consist of same characters.

Example 1:

Input: "abc"
Output: 3
Explanation: Three palindromic strings: "a", "b", "c".
 

Example 2:

Input: "aaa"
Output: 6
Explanation: Six palindromic strings: "a", "a", "a", "aa", "aa", "aaa".
"""
# 回文判断复杂度较高


def countSubstrings(s: str) -> int:

    palind_num = 0
    for i in range(len(s)):
        palind_num += 1
        end = i + 1
        while end < len(s):
            temp_str = s[i:end + 1]
            if is_palindromic(temp_str):
                palind_num += 1
            end += 1
    return palind_num


def is_palindromic(s):
    return s == s[::-1]


print(countSubstrings("aba"))
"""
Runtime: 632 ms, faster than 9.11% of Python3 online submissions for Palindromic Substrings.
Memory Usage: 14.2 MB, less than 72.23% of Python3 online submissions for Palindromic Substrings.
"""