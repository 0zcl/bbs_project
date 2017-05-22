# from django.test import TestCase

# Create your tests here.

for k in {}:
    print("aa")
print("bb")

dict = {'1':2,
        "3":4}
valu = dict.get("1")
print(valu)  # 输出2

if 1 in dict:
    print('hahaha')  # １需加上双引号才会有输出

print("\033[41;1mno msg for [%s][%s],timeout\033[0m" % ("zcl","zcl"))