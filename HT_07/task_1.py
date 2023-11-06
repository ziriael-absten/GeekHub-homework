# 1. Створіть функцію, всередині якої будуть записано список із п'яти користувачів (ім'я 
# та пароль). Функція повинна приймати три аргументи: два - обов'язкових (<username> та
#  <password>) і третій - необов'язковий параметр <silent> (значення за замовчуванням -
#  <False>).
# Логіка наступна:
#     якщо введено коректну пару ім'я/пароль - вертається True;
#     якщо введено неправильну пару ім'я/пароль:
#         якщо silent == True - функція вертає False
#         якщо silent == False -породжується виключення LoginException (його також треба створити =))

class LoginException(Exception):
    def __init__(self, msg):
        self.msg = msg


def login(name, password, silent=False):
    users = {'Anna': '12345', 'Kate': '54321', 'Peter': 'apple123', 'Tom': 'hfvdbrf',
     'Mark': '51531fejb'}
    for key, value in users.items():
        if key == name and value == password:
            return True
    if silent:
        return False
    else:
        raise LoginException("Invalid name and password")


name = input("Enter a name: ")
password = input("Enter a password: ")
silent = input("True/False ")
print(login(name, password, bool(silent)))
