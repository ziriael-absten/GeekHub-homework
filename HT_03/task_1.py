# 1. Write a script that will run through a list of tuples and replace the last value
#  for each tuple. The list of tuples can be hardcoded. The "replacement" value is entered 
#  by user. The number of elements in the tuples must be different.
tuple_lst =  [(), (99,), (1, 2, 3)]
value = input("Enter a value: ")
counter = 0
for i in tuple_lst:
    el = list(tuple_lst[counter])
    if el:
        el[-1] = value
        tuple_lst[counter] = tuple(el)
    counter += 1
# print(tuple_lst)
