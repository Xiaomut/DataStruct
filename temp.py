import copy

def change(num=None, lst_A=None, lst_B=None):
    # num = int(input())
    # lst_A = [int(i) for i in input().split(' ')]
    # lst_B = [int(i) for i in input().split(' ')]
    flag = True
    count = []
    new_lst = []
    for i in range(1, len(lst_A)):
        if lst_A[i] <= lst_A[i-1]:
            new_lst.append(lst_B[i])
            count.append(i-1)
        else:
            new_lst.append(lst_A[i-1])


    for i in range(1, len(new_lst)):
        if new_lst[i] <= new_lst[i-1]:
            flag = False
    
    if flag:
        return len(count)
    else:
        return -1


# distance = max(abs(int(x1)-int(x2)),abs(int(y1)-int(y2)))
def qikvdis(n=None, k=None, lst=None):
    n, k = [int(i) for i in input().split(' ')]
    lst = []
    for i in range(n):
        tmp = input([int(i) for i in input().split(' ')])
        lst.append(tmp)
    count = 0
    for i in range(len(lst)-1):
        for j in range(i, len(lst)):
            distance = max(abs(int(lst[i][0])-int(lst[j][0])), abs(int(lst[i][1])-int(lst[j][1])))
            if distance == k and lst[j] not in lst[:j]:
                count += 1
    return count



if __name__ == "__main__":
    # num = 5
    # A = [1, 8, 3, 6, 7, 5]
    # B = [1, 2, 3, 6, 9, 8]

    # res = change(num, A, B)
    # # res = change()
    # print(res)

    res = qikvdis(3, 1, [[1,1], [2,2], [1,2]])
    print(res)