import sys

n = int(sys.stdin.readline().strip())
records = list(map(int, sys.stdin.readline().strip().split()))
limmit = int(sys.stdin.readline().strip())


def getlimmit(records, total):
    s = 0
    sum_records = sum(records)
    if sum_records < total:
        return -1
    records.sort()
    preSum = 0
    index = 0
    for i in range(len(records)):
        preSum = s
        if i == 0:
            s = records[i] * len(records)
        else:
            s += (records[i] - records[i - 1]) * (len(records) - i)
        if s == total:
            return records[i]
        if s > total:
            index = i
            break
    if index == 0:
        return total // len(records)
    num = len(records) - index
    limmit = (total - preSum) // num
    return limmit + records[index - 1]


# records = [3, 3, 8, 7, 10, 15]
# limmit = 40
print(getlimmit(records, limmit))