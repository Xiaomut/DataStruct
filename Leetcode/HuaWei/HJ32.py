def spread(left,right):
    ans = 0
    global n
    global s
    while left >=0 and right<= n-1 and s[left]==s[right]:
        ans = right-left+1
        left -=1
        right +=1
    return ans

while True:
    try:
        s = input()
        max_ans = 0
        n = len(s)
        for i in range(n):
            ans1 = spread(i, i)
            ans2 = spread(i, i+1)
            max_ans=max(ans1,ans2,max_ans)
        print(max_ans)
    except:
        break
      
