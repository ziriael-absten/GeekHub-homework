# Create a Python program that repeatedly prompts the user for a number until a valid integer 
# is provided. Use a try/except block to handle any ValueError exceptions, and keep asking for
#  input until a valid integer is entered. Display the final valid integer.

while True:
    try:
        num = int(input("Enter a number: "))
        print(f"Number {num} is ok")
        break
    except ValueError:
        print("Enter valid number please")
