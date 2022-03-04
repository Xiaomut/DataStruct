while True:
    try:
        a = float(input().strip())
        epsilon = 0.0001
        low = min(-1.0, a)
        high = max(1.0, a)
        ans = (low + high) / 2
        while abs(ans**3 - a) >= epsilon:
            if ans**3 < a:
                low = ans
            else:
                high = ans
            ans = (low + high) / 2.0
        print('%.1f' % ans)
    except:
        break