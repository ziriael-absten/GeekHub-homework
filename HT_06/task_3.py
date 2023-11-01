# 3. Написати функцию <is_prime>, яка прийматиме 1 аргумент - число від 0 до 1000, и яка 
# вертатиме True, якщо це число просте і False - якщо ні.

import math


def is_prime(number):
    if number < 0 or number > 1000:
        print("Your number is out of range")
        return
    if number <= 1:
        return False
    if number <= 3:
        return True
    if number % 2 == 0 or number % 3 == 0:
        return False
    for i in range(5, int(math.sqrt(number)) + 1, 6):
        if number % i == 0 or number % (i + 2) == 0:
            return False
    return True


num = input("Enter a number from 1 to 1000: ")
try:
    num = int(num)
except ValueError:
    print("Invalid value")
else:
    print(is_prime(num))
