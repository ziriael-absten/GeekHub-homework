# 5. Написати функцію <fibonacci>, яка приймає один аргумент і виводить всі числа Фібоначчі,
#  що не перевищують його.

def fibonacci(num):
    a = 0
    b = 1
    while a <= num:
        print(a)
        temporary = a + b
        a = b
        b = temporary

num = int(input("Enter a number: "))
try:
    num = int(num)
except ValueError:
    try:
        num = float(num)
    except ValueError:
        print("Invalid value")
    else:
        fibonacci(num)
else:
    fibonacci(num)
