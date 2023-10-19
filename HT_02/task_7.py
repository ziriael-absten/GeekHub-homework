# 7. Write a script to concatenate all elements in a list into a string and print it.
#  List must be include both strings and integers and must be hardcoded.
lst = [1, 2, 3, "m", "n", "apple"]
string = [str(item) for item in lst]
string = " ".join(string)
# print(string)



