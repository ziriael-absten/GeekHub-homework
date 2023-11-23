# 1. Створити клас Calc, який буде мати атребут last_result та 4 методи. Методи повинні 
# виконувати математичні операції з 2-ма числами, а саме додавання, віднімання, множення, 
# ділення.
# - Якщо під час створення екземпляру класу звернутися до атребута last_result він повинен 
# повернути пусте значення.
# - Якщо використати один з методів - last_result повенен повернути результат виконання 
# ПОПЕРЕДНЬОГО методу.
#     Example:
#     last_result --> None
#     1 + 1
#     last_result --> None
#     2 * 3
#     last_result --> 2
#     3 * 4
#     last_result --> 6
#     ...
# - Додати документування в клас (можете почитати цю статтю:

class Calc:
    def __init__(self, last_result=None):
        """
        Initialize a Calculator object.
        Parameters:
        - last_result: The initial value for the last result. Default is None.
        """
        self.last_result = last_result
        self.new_result = None


    def addition(self, first, second):
        """
        Perform addition operation.
        Parameters:
        - first: The first operand.
        - second: The second operand.
        Returns:
        The result of the addition operation.
        """
        self.last_result = self.new_result
        self.new_result = first + second
        return self.new_result


    def subtraction(self, first, second):
        """
        Perform subtraction operation.
        Parameters:
        - first: The minuend.
        - second: The subtrahend.
        Returns:
        The result of the subtraction operation.
        """
        self.last_result = self.new_result
        self.new_result = first - second
        return self.new_result


    def multiplication(self, first, second):
        """
        Perform multiplication operation.
        Parameters:
        - first: The first factor.
        - second: The second factor.
        Returns:
        The result of the multiplication operation.
        """
        self.last_result = self.new_result
        self.new_result = first * second
        return self.new_result


    def division(self, first, second):
        """
        Perform division operation.
        Parameters:
        - first: The numerator.
        - second: The denominator.
        Returns:
        The result of the division operation.
        """
        self.last_result = self.new_result
        self.new_result = first / second
        return self.new_result


    def __str__(self) -> str:
        """
        Convert the Calculator object to a string.
        Returns:
        A string representation of the last result.
        """
        return str(self.last_result)


calculator = Calc()
print(calculator)
calculator.addition(1, 1)
print(calculator)
calculator.multiplication(2, 3)
print(calculator)
calculator.multiplication(4, 3)
print(calculator)
