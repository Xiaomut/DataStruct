def toStr(n, base):
    convertString = "0123456789ABCDEF"
    if n < base:
        return convertString[n]
    else:
        return toStr(n//base, base) + convertString[n % base]


s = []
def toStr2(n, base):
    convertString = "0123456789ABCDEF"
    if n < base:
        s.append(convertString[n])
    else:
        s.append(convertString[n % base])
        toStr2(n // base, base)


if __name__ == "__main__":
    # res = toStr(128, 2)
    # print(res)
    toStr2(128, 2)