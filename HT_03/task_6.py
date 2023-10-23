# Write a script to get the maximum and minimum value in a dictionary.
values_dict = {"first": 1, "second": 2, "fruit" : "banana", "letter" : "m", "lst" : ["m", "n", "l"], 
"names" : ["Anna", "Kate"], "data": {"name" : "Peter", "age" : 16}, "prices": {"banana" : 67,
"milk" : 52, "eggs": 32}, "random_tuple" : ("book", "door"), "random_tulpe2" : ("shelf", "window")}
nums_lst = []
str_lst = []
lst_lst = []
dict_lst = []
tuple_lst = []
for value in values_dict.values():
    if isinstance(value, (int, float)):
        nums_lst.append(value)
    elif isinstance(value, str):
        str_lst.append(value)
    elif isinstance(value, (list, tuple)):
        lst_lst.append(list(value))
    elif isinstance(value, dict):
        dict_lst.append(list(value.items()))
print(f"The largest value of numbers is {(max(nums_lst))} and the smallest {min(nums_lst)}")
print(f"The largest value of strings is {(max(str_lst))} and the smallest {min(str_lst)}")
print(f"The largest value of dictionaries is {max(dict_lst)} and the smallest {min(dict_lst)}")
print(f"The largest value of lists and tuples is {(max(lst_lst))} and the smallest {min(lst_lst)}")
