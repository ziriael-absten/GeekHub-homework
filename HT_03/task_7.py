# 7. Write a script which accepts a <number> from user and generates dictionary 
# in range <number> where key is <number> and value is <number>*<number>
#     e.g. 3 --> {0: 0, 1: 1, 2: 4, 3: 9}
num = int(input("Enter a number: "))
nums_dict = {}
for i in range(0, num + 1):
    nums_dict[i] = i * i
# print(nums_dict)

