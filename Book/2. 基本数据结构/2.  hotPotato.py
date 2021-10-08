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


if __name__ == "__main__":
    res = potato(["Bill", "David", "Susan", "Jane", "Kent", "Brad"], 7)
    print(res)