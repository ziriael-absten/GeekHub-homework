# Create a custom exception class called NegativeValueError. Write a Python program that
#  takes an integer as input and raises the NegativeValueError if the input is negative. 
# Handle this custom exception with a try/except block and display an error message.

class NegativeValueError(Exception):
    def __init__(self, value):
        self.value = value
try:
    num = int(input("Enter a number: "))
    if num < 0:
        raise NegativeValueError(num)
    print(f"Your answer is ok :)")
except NegativeValueError as error:
    print(f"Error: {error} is less then 0")
