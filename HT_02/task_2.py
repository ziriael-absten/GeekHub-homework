# 2. Write a script which accepts two sequences of comma-separated colors from user.
#  Then print out a set containing all the colors from color_list_1 which are not present in color_list_2.
color_list_1 = input("Enter some colors: ")
color_list_2 = input("Enter some colors again please: ")
color_list_1 = color_list_1.split(",")
color_list_2 = color_list_2.split(",")
result = list(set(color_list_1) - set(color_list_2))
# print(result)
