def prod(num):
    if num == 1:
        return 1
    else:
        return num * prod(num - 1)


if __name__ == "__main__":
    res = prod(4)
    print(res)