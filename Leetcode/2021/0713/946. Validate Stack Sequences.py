def isPopOrder(pushV, popV):

    m, n = len(pushV), len(popV)
    if m != n:
        return False
    if pushV == [] and popV == []:
        return True

    stack = []
    index = 0

    for item in pushV:
        stack.append(item)
        while popV[index] == stack[-1] and stack:
            stack.pop()
            index += 1

    if stack == []:
        return True
    else:
        return False


if __name__ == "__main__":
    a = [1, 9, 8, 3, 0, 2, 6, 7, 5, 4]
    b = [9, 8, 4, 7, 3, 2, 5, 1, 6, 0]
    print(isPopOrder(a, b))
