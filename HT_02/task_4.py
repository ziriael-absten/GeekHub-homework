# 4. Write a script which accepts a <number>
#  from user and then <number> times asks user for string input. At the end script must print out result of concatenating all <number> strings.
num = int(input("Enter a number: "))
string = ""
for i in range(0, num):
    word = input("Enter a word: ")
    string = string + word + " "
# print(string)

