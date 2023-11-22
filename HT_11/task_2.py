# 2. Створити клас Person, в якому буде присутнім метод __init__ який буде приймати якісь 
# аргументи, які зберігатиме в відповідні змінні.
# - Методи, які повинні бути в класі Person - show_age, print_name, show_all_information.
# - Створіть 2 екземпляри класу Person та в кожному з екземплярів створіть атребут profession 
# (його не має інсувати під час ініціалізації).

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.profession = None


    def show_age(self):
        print(f"{self.name} is {self.age} years old.")


    def print_name(self):
        print(f"Name: {self.name}")


    def show_all_information(self):
        print(f"Name: {self.name}, Age: {self.age}, Profession: {self.profession}")


person1 = Person("Alice", 25)
person2 = Person("Bob", 30)
person1.profession = "Engineer"
person2.profession = "Teacher"
person1.show_all_information()
person2.show_all_information()
