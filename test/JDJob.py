# encoding: utf-8

'''
@author: LiDami
@license: (C) Copyright 2013-2017, BigBigData Manager Corporation Limited.
@contact: li.dami@foxmail.com
@software: MacBookPro
@file: JDJob.py
@time: 2017/9/6 11:01
@desc:
'''

##' 京东：输入两行数，输出去重的排序好的数列'
# ''' join的用法
# str = "-";
# seq = ("a", "b", "c"); # 字符串序列
# print str.join( seq );
# '''
# def setff(a,b):
#     s = set(a+b)
#     l = sorted(list(s))
#     return ' '.join([str(i) for i in l])
# if __name__=='__main__':
#     c = raw_input()
#     A = map(int,raw_input().split())
#     B = map(int,raw_input().split())
#     print setff(A,B)

#进制均值问题
def rev(n):
    result = []
    for i in range(2, n):
        # 商 s,余数 y
        sums = 0
        s = n / i
        y = n % i
        while s != 0:
            sums += y
            y = s % i
            if s < i:
                sums += s
                s = 0
            else:
                s = s / i
        #         这个里面存的是数字n的各种进制的结果
        result.append(sums)
    #     各种进制求和
    result = sum(result)
    # 这边去处最大公约数
    a = result
    b = n - 2
    # 求两个数的最小公约数，思路就是欧几里德算法(辗转相除法)--
    # 若a=bq+r，则（a,b）=（b,r），即a,b的最大公约数等于b,r的最大公约数。
    # 举个例子来说：24=10*2+4，那么(24,10)=(10,4)=2
    while a % b != 0:
        temp = a % b
        a = b
        b = temp
    print b
    return str(result / b) + '/' + str((n - 2) / b)
if __name__ == "__main__":
    while True:
        try:
            n = int(raw_input().strip())
            #            values=map(str,raw_input().strip().split(' '))
            if n < 3:
                break
            else:
                print rev(n)
        except:
            break

