"""递归方案"""
def recMC(coinValueList, change):
    minCoins = change
    if change in coinValueList:
        return 1
    else:
        lst = [c for c in coinValueList if c <= change]
        for i in lst:
            numCoins = 1 + recMC(coinValueList, change-i)
            if numCoins < minCoins:
                minCoins = numCoins
            return minCoins


"""优化后的递归方案"""
def recDC(coinValueList, change, knownResults):
    minCoins = change
    if change in coinValueList:
        knownResults[change] = 1
        return 1
    elif knownResults[change] > 0:
        return knownResults[change]
    else:
        for i in [c for c in coinValueList if c <= change]:
            numCoins = 1 + recDC(coinValueList, change-i, knownResults)
            if numCoins < minCoins:
                minCoins = numCoins
                knownResults[change] = minCoins
    return minCoins


"""
DP方案
numCoins = min(1 + numCoins(originalamount - 1),
            1 + numCoins(originalamount - 5),
            1 + numCoins(originalamount - 10),
            1 + numCoins(originalamount - 25))
"""
def dpMakeChange(coinValueList, change, minCoins):
    for cents in range(change+1):
        coinCount = cents
        for j in [c for c in coinValueList if c <= cents]:
            if minCoins[cents-j] + 1 < coinCount:
                coinCount = minCoins[cents - j]+1
                minCoins[cents] = coinCount
    return minCoins[change]


"""修改后的动态规划解法"""
def dpMakeChange2(coinValueList, change, minCoins, coinsUsed):
    for cents in range(change+1):
        coinCount = cents
        newCoin = 1
        for j in [c for c in coinValueList if c <= cents]:
            if minCoins[cents-j] + 1 < coinCount:
                coinCount = minCoins[cents -j]+1
                newCoin = j
            minCoins[cents] = coinCount
            coinsUsed[cents] = newCoin
    return minCoins[change]


def printCoins(coinsUsed, change):
    coin = change
    while coin > 0:
        thisCoin = coinsUsed[coin]
        print(thisCoin)
        coin = coin - thisCoin


if __name__ == "__main__":
    # res = recMC([1, 5, 10, 25], 63)
    res = dpMakeChange([1, 5, 10, 25], 63, [0] * 64)
    print(res)