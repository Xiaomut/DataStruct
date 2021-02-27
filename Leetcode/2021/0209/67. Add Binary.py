def addBinary(a: str, b: str) -> str:
    # len_a = len(a)
    # len_b = len(b)

    la = [int(i) for i in list(a)][::-1]
    lb = [int(i) for i in list(b)][::-1]
    res = []
    add = 0

    def is_len(l1, l2):
        if len(l1) >= len(l2):
            return l1, l2
        else:
            return l2, l1

    la, lb = is_len(la, lb)
    for num in lb:
        temp_num = num + la[0] + add
        add = 0
        if temp_num == 2:
            temp_num = 0
            add = 1
        elif temp_num == 3:
            temp_num = 1
            add = 1
        res.append(temp_num)
        la.pop(0)
    for num in la:
        temp_num = num + add
        add = 0
        if temp_num == 2:
            temp_num = 0
            add = 1
        res.append(temp_num)
    if add == 1:
        res.append(add)

    return ''.join(str(i) for i in res[::-1])


print(addBinary(a="1010", b="1011"))
