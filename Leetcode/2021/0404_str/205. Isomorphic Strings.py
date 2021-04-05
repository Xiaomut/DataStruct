"""
Given two strings s and t, determine if they are isomorphic.
Two strings s and t are isomorphic if the characters in s can be replaced to get t.
All occurrences of a character must be replaced with another character while preserving the order of characters. No two characters may map to the same character, but a character may map to itself.

Example 1:

Input: s = "egg", t = "add"
Output: true
Example 2:

Input: s = "foo", t = "bar"
Output: false
Example 3:

Input: s = "paper", t = "title"
Output: true
"""


class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:

        s_list = self.func(s)
        t_list = self.func(t)

        return s_list == t_list

    def func(self, temp):
        num = 1
        dics = {}
        temp_list = ''
        for i in temp:
            if i not in dics.keys():
                dics[i] = num
                temp_list += str(num)
                num += 1
            else:
                temp_list += str(dics[i])
        return temp_list


print(isIsomorphic(s="egg", t="add"))
"""
Runtime: 80 ms, faster than 5.66% of Python3 online submissions for Isomorphic Strings.
Memory Usage: 14.7 MB, less than 15.94% of Python3 online submissions for Isomorphic Strings.
"""