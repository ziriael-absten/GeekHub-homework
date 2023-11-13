# 3. Програма-банкомат.
#    Використувуючи функції створити програму з наступним функціоналом:
#       - підтримка 3-4 користувачів, які валідуються парою ім'я/пароль (файл <users.CSV>);
#       - кожен з користувачів має свій поточний баланс (файл <{username}_balance.TXT>) та 
# історію транзакцій (файл <{username_transactions.JSON>);
#       - є можливість як вносити гроші, так і знімати їх. Обов'язкова перевірка введених 
# даних (введено цифри; знімається не більше, ніж є на рахунку і т.д.).
#    Особливості реалізації:
#       - файл з балансом - оновлюється кожен раз при зміні балансу (містить просто цифру з 
# балансом);
#       - файл - транзакціями - кожна транзакція у вигляді JSON рядка додається в кінець 
# файла;
#       - файл з користувачами: тільки читається. Але якщо захочете реалізувати функціонал 
# додавання нового користувача - не стримуйте себе :)
#    Особливості функціонала:
#       - за кожен функціонал відповідає окрема функція;
#       - основна функція - <start()> - буде в собі містити весь workflow банкомата:
#       - на початку роботи - логін користувача (програма запитує ім'я/пароль). Якщо вони 
# неправильні - вивести повідомлення про це і закінчити роботу (хочете - зробіть 3 спроби, а
#  потім вже закінчити роботу - все на ентузіазмі :))
#       - потім - елементарне меню типн:
#         Введіть дію:
#            1. Продивитись баланс
#            2. Поповнити баланс
#            3. Вихід
#       - далі - фантазія і креатив, можете розширювати функціонал, але основне завдання 
# має бути повністю реалізоване :)
#     P.S. Увага! Файли мають бути саме вказаних форматів (csv, txt, json відповідно)
#     P.S.S. Добре продумайте структуру програми та функцій (edited)

import csv
import json


def view_balance(name):
    with open(f"{name}_balance.txt") as user_file:
        content = user_file.read()
        print()
        print(f"{content} UAH on your balance")
        print()


def deposit(name):
    with open(f"{name}_balance.txt", "r+") as user_file:
        content = user_file.read()
        user_file.seek(0)
        amount = float(input("Enter a sum you want to deposit: "))
        if amount < 0:
            print("Deposit should be more then 0")
            return
        if isinstance(amount, (int, float)):
            total = round(float(content) + amount, 2)
            new_transaction = {"name": name, "operation": "deposit", "amount": amount, "balance" : total}
            user_file.write(str(total))
            with open(f"{name}_transactions.json", 'r+') as json_file:
                transactions = json.load(json_file)
                transactions.append(new_transaction)
                json_file.seek(0)
                json.dump(transactions, json_file)


def withdraw(name):
    with open(f"{name}_balance.txt", "r+") as user_file:
        content = user_file.read()
        user_file.seek(0)
        amount = float(input("Enter a sum you want to withdraw: "))
        if amount < 0:
            print("Amount should be more then 0")
            return
        if isinstance(amount, (int, float)) and amount <= float(content):
            result = round(float(content) - amount, 2)
            new_transaction = {"name": name, "operation": "withdraw", "amount": amount, "balance" : result}
            user_file.write(str(result))
            with open(f"{name}_transactions.json", 'r+') as json_file:
                transactions = json.load(json_file)
                transactions.append(new_transaction)
                json_file.seek(0)
                json.dump(transactions, json_file)


def start(name):
    while True:
        print("To view the balance 1\n"+
        "To deposit 2\n"+
        "To withdraw 3\n"+
        "Exit 4\n")
        try:
            command = int(input("Enter your command please: "))
        except ValueError:
            print("Command must be a number")
            continue
        if command == 1:
            view_balance(name)
        elif command == 2:
            deposit(name)
        elif command == 3:
            withdraw(name)
        elif command == 4:
            break
        else:
            print("Your command is not correct")


def login():
    name = input("Enter your name: ")
    password = input("Enter your password: ")
    with open("users.CSV") as login_file:
        csv_reader = csv.reader(login_file)
        for row in csv_reader:
            if row[0] == name and row[1] == password:
                start(name)
                return
        print("User not found")


if __name__ == "__main__":
    login()
