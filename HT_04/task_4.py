# Write a Python program that demonstrates exception chaining. Create a custom exception class
#  called CustomError and another called SpecificError. In your program (could contain any 
# logic you want), raise a SpecificError, and then catch it in a try/except block, re-raise 
# it as a CustomError with the original exception as the cause. Display both the custom error 
# message and the original exception message.
class SpecificError(Exception):
    pass
class CustomError(Exception):
    pass
num = int(input("Enter a number between 1 and 100 : "))
try:
    if num < 1 or num > 100:
        raise SpecificError("Your number is out of range")
    print("I like your number:)")
except SpecificError as error1:
    try:
        raise CustomError("You should choose number only between 1 and 100")
    except CustomError as error2:
        print(error1)
        print(error2)
