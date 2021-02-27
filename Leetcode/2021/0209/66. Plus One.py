def plusOne(digits):
    length = len(digits)
    num = int(''.join(str(i) for i in digits)) + 1
    res = [int(i) for i in str(num)]
    if len(res) == length:
        return res
    else:
        return [0] * (length - len(res)) + res


print(plusOne([9, 9, 9]))
