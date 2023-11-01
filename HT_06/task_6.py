# 6. Написати функцію, яка буде реалізувати логіку циклічного зсуву елементів в списку. 
# Тобто функція приймає два аргументи: список і величину зсуву (якщо ця величина додатня - 
# пересуваємо з кінця на початок, якщо від'ємна - навпаки - пересуваємо елементи з початку 
# списку в його кінець).
#    Наприклад:
#    fnc([1, 2, 3, 4, 5], shift=1) --> [5, 1, 2, 3, 4]
#    fnc([1, 2, 3, 4, 5], shift=-2) --> [3, 4, 5, 1, 2]

def change_lst(lst, shift):
    start = lst[-(shift):]
    end = lst[:-(shift)]
    result = start + end
    return result

print(change_lst([1, 2, 3, 4, 5], -2))
