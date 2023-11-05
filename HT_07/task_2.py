# 2. Створіть функцію для валідації пари ім'я/пароль за наступними правилами:
#    - ім'я повинно бути не меншим за 3 символа і не більшим за 50;
#    - пароль повинен бути не меншим за 8 символів і повинен мати хоча б одну
#    цифру;
#    - якесь власне додаткове правило :)
#    Якщо якийсь із параментів не відповідає вимогам - породити виключення із відповідним текстом.

class NameException(Exception):
    def __init__(self, name):
        self.name = name


class PasswordException(Exception):
    def __init__(self, password):
        self.password = password


class SpaceException(Exception):
    pass


def check_login(name, password):
    if len(name) < 3 or len(name) > 50:
        raise NameException(name)
    num_in_password = False
    for i in password:
        if i.isdigit():
            num_in_password = True
            break
    if len(password) < 8 or num_in_password == False:
        raise PasswordException(password)
    if " " in name or " " in password:
        raise SpaceException()


name = input("Enter a name: ")
password = input("Enter a password: ")
try:
    check_login(name, password)
except NameException as e:
    print(f"Name {e} is not valid")
except PasswordException as e2:
    print(f"Password {e2} is not valid")
except SpaceException:
    print("You shouldn't use spaces in your name or password")
    