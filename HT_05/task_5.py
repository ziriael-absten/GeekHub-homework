# 5. Ну і традиційно - калькулятор :slightly_smiling_face: Повинна бути 1 ф-цiя, 
# яка б приймала 3 аргументи - один з яких операцiя, яку зробити! Аргументи брати від 
# юзера (можна по одному - 2, окремо +, окремо 2; можна всі разом - типу 1 + 2). Операції 
# що мають бути присутні: +, -, *, /, %, //, **. Не забудьте протестувати з різними 
# значеннями на предмет помилок!

def calculation(a, b, operation):
    if operation == "+":
        return a + b
    elif operation == "-":
        return a - b
    elif operation == "*":
        return a * b
    elif operation == "/":
        if b == 0:
            return "Zero division error"
        return a / b
    elif operation == "%":
        if b == 0:
            return "Zero division error"
        return a % b
    elif operation == "//":
        if b == 0:
            return "Zero division error"
        return a // b
    elif operation == "**":
        return a ** b
    else:
        return "Invalid operation"

first = input("Enter first num: ")
second = input("Enter second num: ")
operation = input("Enter an operation(+, -, *, /, %, //, **): ")
try:
    first = int(first)
    second = int(second)
except ValueError:
    try:
        first = float(first)
        second = float(second)
    except ValueError:
        print("Invalid values")
    else:
        result = calculation(first, second, operation)
        print(f"Result of operation {first} {operation} {second} is {result}")
else:
    result = calculation(first, second, operation)
    print(f"Result of operation {first} {operation} {second} is {result}")
