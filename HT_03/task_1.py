# 1. Write a script that will run through a list of tuples and replace the last value
#  for each tuple. The list of tuples can be hardcoded. The "replacement" value is entered 
#  by user. The number of elements in the tuples must be different.
tuple_lst = [(1, 2, 3, 4, 5), ("m", True, 2.2, False), ("apple", "banana", "orange"), (1, [])]
value = input("Enter a value: ")
for i in range(0, len(tuple_lst)):
    el = list(tuple_lst[i])
    el[-1] = value
    tuple_lst[i] = tuple(el)
# print(tuple_lst)

