

def divide(decNumber, num):
    remstack = []
    if num == 16:
        digits = "0123456789ABCDEF"
    else:
        digits = "0123456789"

    while decNumber > 0:
        rem = decNumber % num
        remstack.append(rem)
        decNumber = decNumber // num

    res = ""
    for i in remstack[::-1]:
        res = res + digits[i]
    return res


if __name__ == "__main__":
    res = divide(24, 2)
    print(res)