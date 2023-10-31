# 3. Користувач вводить змiннi "x" та "y" з довiльними цифровими значеннями. 
# Створiть просту умовну конструкцiю (звiсно вона повинна бути в тiлi ф-цiї), пiд час 
# виконання якої буде перевiрятися рiвнiсть змiнних "x" та "y" та у випадку 
# нервіності - виводити ще і різницю.
    # Повиннi опрацювати такi умови (x, y, z заміність на відповідні числа):
    # x > y;       вiдповiдь - "х бiльше нiж у на z"
    # x < y;       вiдповiдь - "у бiльше нiж х на z"
    # x == y.      вiдповiдь - "х дорiвнює z"

def compare(x, y):
    if x == y:
        return "x is equal to z"
    if x > y:
        z = x - y
        return f"{x} is greater than {y} by {z}"
    else:
        z = y - x
        return f"{y} is greater than {x} by {z}"

x = input("Enter a first number: ")
y = input("Enter a second number: ")
try:
    x = int(x)
    y = int(y)
except ValueError:
    try:
        x = float(x)
        y = float(y)
    except ValueError:
        print("Invalid values")
    else:
        print(compare(x, y))
else:
    print(compare(x, y))
