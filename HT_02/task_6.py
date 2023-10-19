# 6. Write a script to check whether a value from user input is contained in a group of values.
    # e.g. [1, 2, 'u', 'a', 4, True] --> 2 --> True
        #  [1, 2, 'u', 'a', 4, True] --> 5 --> False
lst = [1, 2, 'u', 'a', 4, True]
value = input("Enter a value: ")
if value in lst:
    result = True
if value.isdigit():
    if int(value) in lst or value in lst:
        result = True
# print(result)


