def cycleStringInclude(s1, s2):
    s1 = s1 + s1
    if s2 in s1:
        return True
    return False


print(cycleStringInclude(s1='AABCD', s2='CDAA'))
