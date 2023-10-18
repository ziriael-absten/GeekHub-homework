lst = [1, 2, 'u', 'a', 4, True]
value = input("Enter a value: ")
if value in lst:
    result = True
if value.isdigit():
    if int(value) in lst or value in lst:
        result = True
# print(result)


