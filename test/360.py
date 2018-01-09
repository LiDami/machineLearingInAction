# -*- coding:utf8 -*-


import sys

if __name__ == "__main__":
    # 读取第一行的n
    a = raw_input('')
    b = raw_input('')
    c = a +' '+ b
    print c
    ans = 0
    for i in range(c):
        # 读取每一行
        line = sys.stdin.readline().strip()
        print type(line)
        # line = line[]
        # 把每一行的数字分隔后转化成int列表
        values = map(int, line.split())
        print type(values)

        for v in values:
            ans += v
    print ans








# n = input('出场数:')
# str = raw_input("请输入:")
# lst1 = str.split(" ")
#
#
# for a in lst1:
#     a = [int(a)]
#     b = len(b)














# str = raw_input("请输入总数:")
# lst1 = str.split(" ")
# # print int(lst1[1])+int(lst1[0])
# str = raw_input("请输入根数:")
# lst2 = str.split(" ")
#
# str = raw_input("请输入价格:")
# lst3 = str.split(" ")
#
# c = 0
# a = int(lst2[0])
# b = int(lst2[1])
# if(a<=int(lst1[0])&b<int(lst1[0])):
#     c += int(lst2[0])*int(lst3[0])+ int(lst2[1])*int(lst3[0])
#     a+=1
#     b+=1
# print c
#
# c1 = 0
# a1 = int(lst2[2])
# if(a1<=int(lst1[1])):
#     c1 += int(lst2[2])*int(lst3[1])
#     a1+=1
# print c1
#
# c2 = 0
# a2 = int(lst2[3])
# if(a2<=int(lst1[0])):
#     c2 += int(lst2[3])*int(lst3[2])
#     a2+=1
# print c2
#
# print max(c,c1,c2)