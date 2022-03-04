n = 2
m = [1, 2]
x = [2, 1]
res = []
for i in range(n):
    for j in range(x[i]):
        res.append(m[i])

weight = {0}
for i in res:
    for j in list(weight):
        tmp = i + j
        weight.add(i + j)
print(len(weight))
