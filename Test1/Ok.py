# for x in "abcd17":
#     if x == "17":
#         break
#     else:
#         print(x)
#
# s = "45"
# p = s + str(23 + 1)
# print(p)


# def binarySearch(alist, item):
#     first = 0
#     last = len(alist) - 1
#     found = False
#
#     while first <= last and not found:
#         midpoint = (first + last) // 2
#         if alist[midpoint] == item:
#             found = True
#         else:
#             if item < alist[midpoint]:
#                 last = midpoint - 1
#             else:
#                 first = midpoint + 1
#
#     return found
#
#
# testlist = [0, 1, 2, 8, 13, 17, 19, 32, 42,]
# print(binarySearch(testlist, 3))
# print(binarySearch(testlist, 13))


# def finde(string_input):
#     for x in string_input:
#         if x == 'E' or x == 'e':
#             print(x)
#
#
# finde("eErEFHJ")


# s = "abc def ghi jkl"
# print(s[-2], s[-3], s[-4])
# print(s.find('j'))

# s = ['a', 'b', 'c']
# s[0] = "x"
# print(s)

# y = 0
# if False:
#     x = 8/y
#     print(x)

# x = 'A'
# print(x > 'a')
#
# def recAdd(n):
#     if n > 0:
#         return n * recAdd(n - 1)


# print(recAdd(4))

# def factorial( n ):
#    if n <1:   # base case
#        return 1
#    else:
#        return n * factorial( n - 1 )  # recursive call
#
#
# # def factorial(n):
# #     if n < 1:  # base case
# #         return n * factorial(n - 1)  # recursive call
#
#
# print(factorial(5))


# d = dict()
# d[1] = "a"
# print(d)
# d["a"] = 1
# print(d)
# d[1] = "b"
# print(d)
#
# # d2 = dict()
# print(d["a"])


# def fibTail(n, a=0, b=1):
#     if n == 0:
#         return a
#     if n == 1:
#         return b
#     return fibTail(n - 1, b, a + b);
#
#
# n = 6;
# print("fibTail(" + str(n) + ") = " + str(fibTail(n)))
#
#
# def fibTrad(n):
#     if n < 2:
#         return n
#     return fibTrad(n-2) + fibTrad(n-1)
#
#
# print(fibTrad(4) + fibTrad(6))


def cal(n, acc=1):
    print(acc)
    if n == 0:
        return 100
    elif n == 1:
        return 2
    else:
        return cal(n-1, acc*8)


cal(4)


s = "Hello World"
print((s[1]))
print(s.find("g"))
print(s.index("g"))
print("1""2")

