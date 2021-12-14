from collections import deque


def potato(names, num):
    q = deque()
    for name in names:
        q.append(name)

    while len(q) > 1:
        for i in range(num):
            q.append(q.popleft())
        q.popleft()
    return q.popleft()


def LastRemaining_Solution(n, m):
    if n <= 0:
        return -1
    x = 0
    for i in range(2, n + 1):
        x = (x + m) % i
    return x


if __name__ == "__main__":
    # res = potato(["Bill", "David", "Susan", "Jane", "Kent", "Brad"], 7)
    # print(res)

    res = LastRemaining_Solution(5, 3)
    print(res)