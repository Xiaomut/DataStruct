def lengthOfLongestSubstring(s: str) -> int:
    from collections import Counter
    length = len(s)
    if length <= 1:
        return length
    l, r = 0, 1
    res = 0
    while r <= length:
        if l >= r:
            r += 1
            continue
        string = s[l:r]
        print(f'l: {l} r: {r} string: {string}')
        c = dict(Counter(string))
        x = max(list(c.values()))
        if x > 1:
            l += 1
        else:
            res = max(res, r - l)
            r += 1
    return res


if __name__ == "__main__":
    s = 'pwwkew'
    res = lengthOfLongestSubstring(s)
    print(res)