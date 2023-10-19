# 3. Write a script which accepts a <number>
#  from user and print out a sum of the first <number> positive integers.
num = int(input("Enter a number: "))
if num > 0:
    total = 0
    for i in range(1, num + 1):
        total += i
# print(total)

