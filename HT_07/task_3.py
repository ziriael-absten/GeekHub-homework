# 3. На основі попередньої функції (скопіюйте кусок коду) створити наступний скрипт:
#    а) створити список із парами ім'я/пароль різноманітних видів (орієнтуйтесь по правилам 
#    своєї функції) - як валідні, так і ні;
#    б) створити цикл, який пройдеться по цьому циклу і, користуючись валідатором, перевірить 
#    ці дані і надрукує для кожної пари значень відповідне повідомлення, наприклад:
#       Name: vasya
#       Password: wasd
#       Status: password must have at least one digit
#       -----
#       Name: vasya
#       Password: vasyapupkin2000
#       Status: OK
#    P.S. Не забудьте використати блок try/except ;)

class NameTooShort(Exception):
    def __init__(self, name):
        self.name = name


class NameTooLong(Exception):
    def __init__(self, name):
        self.name = name


class PasswordTooShort(Exception):
    def __init__(self, password):
        self.password = password


class DigitInPassword(Exception):
    def __init__(self, password):
        self.password = password


users = [("An", "12345678"), ("Kate", "67854321"), 
("Petermdhhhhhhewjjedjewhjwjjwehdwebndhejrfehhejhrhrjeh", "apple123"), ("Tom", "hfvdbrfdd"),
 ("Mark", "51531")]
     
def check_name(name):
    if len(name) < 3:
        raise NameTooShort(name)
    if len(name) > 50:
        raise NameTooLong(name)


def check_password(password):
    num_in_password = False
    for i in password:
        if i.isdigit():
            num_in_password = True
            break
    if len(password) < 8:
        raise PasswordTooShort(password)
    if num_in_password == False:
        raise DigitInPassword(password)


for i in users:
    print(f"Name: {i[0]}")
    print(f"Password: {i[1]}")
    try:
        check_name(i[0])
        check_password(i[1])
        print("Status: OK")
    except NameTooShort:
        print("Status: your name is too short")
    except NameTooLong:
        print("Status: your name is too long")
    except PasswordTooShort:
        print("Status: your password is too short")
    except DigitInPassword:
        print("Status: password must have at least one digit")
    print("-----")
