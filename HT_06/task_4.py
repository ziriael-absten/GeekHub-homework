# 4. Написати функцію <prime_list>, яка прийматиме 2 аргументи - початок і кінець діапазона,
#  і вертатиме список простих чисел всередині цього діапазона. Не забудьте про перевірку на 
# валідність введених даних та у випадку невідповідності - виведіть повідомлення.

import math


def prime_list(start, end):
    if start > end or start < 1:
        print("Invalid values")
        return []
    result = []
    for number in range(start, end + 1):
        if number <= 1:
            continue
        if number <= 3:
            result.append(number)
        if number % 2 == 0 or number % 3 == 0:
            continue
        is_prime = True
        for i in range(5, int(math.sqrt(number)) + 1, 6):
            if number % i == 0 or number % (i + 2) == 0:
                is_prime = False
                break
        if is_prime:
            result.append(number)

    return result


start = input("Enter initial value: ")
end = input("Enter the last value: ")
try:
    start = int(start)
    end = int(end)
except ValueError:
    print("Invalid value")
else:
    print(prime_list(start, end))
