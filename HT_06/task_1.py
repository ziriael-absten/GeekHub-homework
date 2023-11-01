# 1. Написати функцію <square>, яка прийматиме один аргумент - сторону квадрата, і
#  вертатиме 3 значення у вигляді кортежа: периметр квадрата, площа квадрата та його 
# діагональ.

import math


def square(num):
    perimeter = num * 4
    area = num * num
    diagonal = num * math.sqrt(2)

    return perimeter, area, diagonal

num = input("Enter the length of the square's side: ")
try:
    num = int(num)
except ValueError:
    try:
        num = float(num)
    except ValueError:
        print("Invalid values")
    else:
        print(square(num))
else:
    print(square(num))
    