# print("please print something")
# input_data(a)=input("please input something:" )
#
# print(input_data)


#///查找最大值及其下标

# a = int(input())
#
# b = list(map(int,input("请输入一串以空格为间隔的数字:\n").split(" ")))
#
# print(max(b),b.index(max(b)))

#//map
# b = map(list,[2,4,6],[1,3,5])
# print(b)

str1 = input("input a string:\n")
a,b = map(str,input("two single string；\n").split(" "))
#s=str1的反向
s = str1[::-1]

#字符串倒序查询 先查到的先输出（按字符串顺序）
for i in range(0,len(s)):
    if s[i] == b:
        print(len(s)-i-1,b)
    elif s[i] == a:
        print(len(s)-i-1,a)

#字符串倒序查询 且 输出倒序（先输出b后a）
# for i in range(0,len(s)):
#     if s[i] == b:
#         print(len(s)-i-1,b)
# for i in range(0,len(s)):
#     if s[i] == a:
#         print(len(s)-i-1,a)
