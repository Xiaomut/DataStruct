"""
Given two strings s and t, return true if t is an anagram of s, and false otherwise.

Example 1:

Input: s = "anagram", t = "nagaram"
Output: true
Example 2:

Input: s = "rat", t = "car"
Output: false
"""


def isAnagram(s: str, t: str) -> bool:
    # s = list(s)
    # t = list(t)
    if len(s) != len(t):
        return False

    dics = {}
    for i in s:
        if i not in dics.keys():
            dics[i] = 1
        else:
            dics[i] += 1
    for j in t:
        if j not in dics.keys():
            return False
        else:
            dics[j] -= 1
    for k in dics.values():
        if k != 0:
            return False
    return True


print(isAnagram("rat", t="car"))
