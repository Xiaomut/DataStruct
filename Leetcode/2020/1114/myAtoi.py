#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   myAtoi.py
@Time    :   2020/11/14 14:14:52
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''

"""8. String to Integer (atoi)"""

def myAtoi(s):
    
    s = s.strip()
    nums_list = list('-+0123456789')
    nums = list('0123456789')
    symbol = ['+', '-']

    if s == "" or s[0] not in nums_list:
        return 0
    try:
        num = int(s)
        if -2**31 > num:
            return -2**31
        elif 2**31<=num:
            return 2**31 -1 
        else:
            return num
    except:
        pass

    if s[0] in symbol:
        output = s[0]
        for i in s[1:]:
            if i in nums:
                output += i
            else:
                break
    else:
        output = ''
        for i in s:
            if i in nums:
                output += i
            else:
                break

    # print(output)
    if output[0] in symbol and len(output) == 1:
        return 0
    num = int(output)
    if -2**31 > num:
        return -2**31
    elif 2**31<=num:
        return 2**31 -1 
    else:
        return num


print(myAtoi("-12"))