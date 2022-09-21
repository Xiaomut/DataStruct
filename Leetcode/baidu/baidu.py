s = "bbaiduabaiduoxiaojiabankanjiaran"

# s = input()


def is_correct(alpha):
    if len(set(alpha)) != 5:
        return False

    yuan = list("aeiou")
    if alpha[0] not in yuan and alpha[3] not in yuan and alpha[
            1] in yuan and alpha[2] in yuan and alpha[4] in yuan:
        return True

    return False


res = 0
if len(s) < 5:
    print(res)
else:
    for i in range(0, len(s)):
        if s[i] in list("aeiou"):
            continue
        else:
            break
    for left in range(i, len(s), 1):
        cur = s[left:left + 5]
        if len(cur) == 5 and is_correct(cur):
            res += 1
    print(res)