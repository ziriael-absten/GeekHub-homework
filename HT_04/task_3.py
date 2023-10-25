# Create a Python script that takes an age as input. If the age is less than 18 or greater 
# than 120, raise a custom exception called InvalidAgeError. Handle the InvalidAgeError by 
# displaying an appropriate error message.
class InvalidAgeError(Exception):
    def __init__(self, age):
        self.age = age
try:
    age = int(input("Enter your age: ")) 
    if age < 18 or age > 120:
        raise InvalidAgeError(age)
    print(f"Your age is: {age}")
except InvalidAgeError as error:
    print(f"Error: {error} is not a valid age. Age should be between 18 and 120.")
