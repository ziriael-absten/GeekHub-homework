# Банкомат 2.0
    # - усі дані зберігаються тільки в sqlite3 базі даних. Більше ніяких файлів. Якщо в 
    # попередньому завданні ви добре продумали структуру програми то у вас не виникне 
    # проблем швидко адаптувати її до нових вимог.
    # - на старті додати можливість залогінитися або створити новго користувача (при 
    # створенні новго користувача, перевіряється відповідність логіну і паролю мінімальним 
    # вимогам. Для перевірки створіть окремі функції)
    # - в таблиці (базі) з користувачами має бути створений унікальний користувач-інкасатор,
    #  який матиме розширені можливості (домовимось, що логін/пароль будуть admin/admin щоб 
    # нам було простіше перевіряти)
    # - банкомат має власний баланс
    # - кількість купюр в банкоматі обмежена. Номінали купюр - 10, 20, 50, 100, 200, 500, 
    # 1000
    # - змінювати вручну кількість купюр або подивитися їх залишок в банкоматі може лише 
    # інкасатор
    # - користувач через банкомат може покласти на рахунок лише сумму кратну мінімальному 
    # номіналу що підтримує банкомат. В іншому випадку - повернути "здачу" (наприклад при 
    # поклажі 1005 --> повернути 5). Але це не має впливати на баланс/кількість купюр 
    # банкомату, лише збільшуєтсья баланс користувача (моделюємо наявність двох незалежних 
    # касет в банкоматі - одна на прийом, інша на видачу)
    # - зняти можна лише в межах власного балансу, але не більше ніж є всього в банкоматі.
    # - при неможливості виконання якоїсь операції - вивести повідомлення з причиною (не 
    # вірний логін/пароль, недостатньо коштів на раунку, неможливо видати суму наявними 
    # купюрами тощо.)

import sqlite3

class NegativeValueError(Exception):
    def __init__(self, value):
        self.value = value

class LoginError(Exception):
    def __init__(self, value):
        self.value = value


con = sqlite3.connect('atm.db')
cur = con.cursor()


def create_tables():
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        balance INTEGER NOT NULL DEFAULT 0,
        is_incasator BOOLEAN NOT NULL
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        type TEXT NOT NULL, 
        amount INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS atm (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tens INTEGER NOT NULL DEFAULT 0,
        twenties INTEGER NOT NULL DEFAULT 0,
        fifties INTEGER NOT NULL DEFAULT 0,
        hundreds INTEGER NOT NULL DEFAULT 0,
        two_hundreds INTEGER NOT NULL DEFAULT 0,
        five_hundreds INTEGER NOT NULL DEFAULT 0,
        thousands INTEGER NOT NULL DEFAULT 0
    )""")
    con.commit()

def insert_tables():
    cur.execute("""
    INSERT OR IGNORE INTO users(username, password, is_incasator) VALUES 
        ('Bob', '12345', FALSE),
        ('Alice', 'password', FALSE),
        ('Alex', '54321', FALSE),
        ('admin', 'admin', TRUE)
    """)

    cur.execute("""
    INSERT OR IGNORE INTO 
    atm(id, tens, twenties, fifties, hundreds, two_hundreds, five_hundreds, thousands) 
    VALUES (1, 20, 20, 20, 20, 20, 20, 20)
    """)
    con.commit()

def incasator_menu():
    print("hello incasator")


def login(username, login_password):
    cur.execute("""
    SELECT id, username, password, is_incasator 
    FROM users WHERE username = ?""", (username, ))
    user_data = cur.fetchone()
    if not user_data:
        raise LoginError("User not found")
    user_id, username, password, is_incasator = user_data
    if login_password != password:
        raise LoginError("Password incorrect")
    return user_id, is_incasator


def register(username, password):
    cur.execute("""
    INSERT OR IGNORE INTO users(username, password, is_incasator) VALUES 
        (?, ?, FALSE)
    """, (username, password))
    con.commit()
    print("Registration successful")


def view_balance(username):
    pass

def deposit():
    pass

def withdraw():
    pass

def read_num():
    num = int(input("Enter amount: "))
    if num < 0:
        raise NegativeValueError(num)
    return num


def user_menu(username):
    while True:
        print("To view the balance 1")
        print("To deposit enter 2")
        print("To withdraw enter 3")
        print("Exit 4")
        command = input("Enter your operation: ")
        if command == "1":
            view_balance(username)
        elif command == "2":
            try:
                amount = read_num()
                deposit(username, amount)
            except ValueError:
                print("Enter a number please")
            except NegativeValueError:
                print("Your number should be bigger than 0")
        elif command == "3":
            try:
                amount = read_num()
                withdraw(username, amount)
            except ValueError:
                print("Enter a number please")
            except NegativeValueError:
                print("Your number should be bigger than 0")
        elif command == 4:
            break
        else:
            print("Your command is not correct")


def start():
    create_tables()
    insert_tables()
    while True:
        print("Login 1\n"+
        "Register 2\n"+
        "Exit 3")
        command = input("Enter your command: ")
        if command == "1":
            username = input("Enter your name: ")
            password = input("Enter your password: ")
            try:
                user_id, is_incasator = login(username, password)  
                if is_incasator:
                    incasator_menu()
                else:
                    user_menu()
            except LoginError as e:
                print(e)
        elif command == "2":
            username = input("Enter your name: ")
            password = input("Enter your password: ")
            # функція перевірки валідностіі
            register(username, password)
        elif command == "3":
            break
        else:
            print("Your command is not correct")


if __name__ == "__main__":
    start()