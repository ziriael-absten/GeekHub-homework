# Write a script to get the maximum and minimum value in a dictionary.
values_dict = {"first": 1, "second": 2, "fruit" : "banana", "letter" : "m", "lst" : ["m", "n", "l"]}
max_value = values_dict["first"]
min_value = values_dict["first"]
min_res = values_dict["first"]
max_res = values_dict["first"]
for value in values_dict.values():
    if isinstance(value, int):
        if max_res < value:
            max_res = value
            max_value = value
        if min_value > value:
            min_res = value
            min_value = value
    else:
        total = 0
        for i in value:
            total += ord(i)
        if total > max_res:
            max_res = total
            max_value = value
        if min_value > total:
            min_res = total
            min_value = value
# print(max_value)
# print(min_value)
