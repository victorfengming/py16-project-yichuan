


def ShowPages(count,p):
    '''
    count  总页数
    p      当前页
    '''
    start = p-5
    end = p+4

    # 判断 如果当前页 小于 5
    if p <= 5:
        start = 1
        end = 10
    # 判断 如果当前页 大于 总页数-5
    if p > count-5:
        start = count-9
        end = count
    # 判断 如果总页数 小于 10
    if count < 10:
        start = 1
        end = count
    for x in range(start,end+1):
        print(x,',',end='')
    
    print()


ShowPages(100,1)
ShowPages(100,2)
ShowPages(100,3)
ShowPages(100,4)
ShowPages(100,5)
ShowPages(100,6)
ShowPages(100,7)
ShowPages(100,20)
ShowPages(100,95)
ShowPages(6,3)
ShowPages(64,10)

