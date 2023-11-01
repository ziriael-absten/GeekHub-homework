# 7. Написати функцію, яка приймає на вхід список (через кому), підраховує кількість 
# однакових елементів у ньомy і виводить результат. Елементами списку можуть бути дані 
# будь-яких типів.
# Наприклад:
# 1, 1, 'foo', [1, 2], True, 'foo', 1, [1, 2] ----> "1 -> 3, foo -> 2, [1, 2] -> 2, True -> 1"

def counter(lst):
    count_dict = {}
    for item in lst:
        if isinstance(item, (list, bool)):
            item = str(item)
        if item in count_dict.keys():
            count_dict[item] += 1
        else:
            count_dict[item] = 1
    for key, value in count_dict.items():
        print(f"{key} -> {value}")

counter([1, 1, 'foo', [1, 2], True, 'foo', 1, [1, 2]])
