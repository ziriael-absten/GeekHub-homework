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


class UserNotFoundError(Exception):
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
        action TEXT NOT NULL, 
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


def add_transaction(user_id, action, amount):
    cur.execute("""
    INSERT INTO transactions(user_id, action, amount) VALUES 
        (?, ?, ?)
    """, (user_id, action, amount))


def show_transactions(user_id):
    cur.execute("""
    SELECT action, amount 
    FROM transactions WHERE user_id = ?""", (user_id, ))
    transactions = cur.fetchall()
    for t in transactions:
        action, amount = t
        print(f"{action} : {amount} UAH")


def atm_balance():
    tens, twenties, fifties, hundreds, two_hundreds, five_hundreds, thousands = get_atm_banknotes()
    print(f"10: {tens}")
    print(f"20: {twenties}")
    print(f"50: {fifties}")
    print(f"100: {hundreds}")
    print(f"200: {two_hundreds}")
    print(f"500: {five_hundreds}")
    print(f"1000: {thousands}")
    total = calc_atm_balance(tens, twenties, fifties, hundreds, two_hundreds, five_hundreds, thousands)
    print(f"Total balance: {total}")


def get_atm_banknotes():
    cur.execute("""
    SELECT tens, twenties, fifties, hundreds, two_hundreds, five_hundreds, thousands 
    FROM atm WHERE id = 1""")
    return cur.fetchone()


def calc_atm_balance(tens, twenties, fifties, hundreds, two_hundreds, five_hundreds, thousands):
    return tens * 10 + twenties * 20 + fifties * 50 + hundreds * 100 + \
    two_hundreds * 200 + five_hundreds * 500 + thousands * 1000


nominal_names = {"10": "tens", "20": "twenties", "50": "fifties", "100": "hundreds",
 "200": "two_hundreds", "500": "five_hundreds", "1000": "thousands"}

 
def add_banknotes():
    while True:
        nominal = input("Choose a nominal 10/20/50/100/200/500/1000 or type 'exit'\n")
        if nominal == "exit":
            break
        if nominal not in nominal_names:
            print(f"Invalid nominal: {nominal}")
            continue
        try:
            amount = read_positive_num(f"Enter a number of {nominal} ")
        except ValueError:
            print("Please enter a valid number")
            continue
        except NegativeValueError:
            print("Please enter a not negative number")
            continue
        nominal_name = nominal_names[nominal]
        cur.execute(f"UPDATE atm SET {nominal_name} = ?", (amount,))
    con.commit()


def incasator_menu():
    while True:
        print("--------------")
        print("To view the atm balance enter 1")
        print("To set banknotes enter 2")
        print("Exit 3")
        print("--------------")
        command = input("Enter your operation: ")
        if command == "1":
            atm_balance()
        elif command == "2":
            add_banknotes()
        elif command == "3":
            break
        else:
            print("Your command is not correct")


def validate_registration(name, password):
    if len(name) < 2: 
        print("Your name should be longer than 2 letters")
        return False
    if len(name) > 50:
        print("Your name should be shorter than 50 letters")
        return False
    num_in_password = False
    for i in password:
        if i.isdigit():
            num_in_password = True
            break
    if len(password) < 8:
        print("Your password should be longer than 8 symbols")
        return False
    if num_in_password == False:
        print("Your password should contain at least one digit")
        return False
    return True


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


def view_balance(user_id):
    balance = get_balance(user_id)
    print(f"Your balance is {balance} UAH")


def get_balance(user_id):
    cur.execute("""
    SELECT balance 
    FROM users WHERE id = ?""", (user_id, ))
    user_data = cur.fetchone()
    if not user_data:
        raise UserNotFoundError("User not found")
    return user_data[0]


def deposit(user_id):
    try:
        requested_amount = read_positive_num("Enter amount: ")
    except ValueError:
        print("Enter a number please")
        return
    except NegativeValueError:
        print("Your number should be bigger than 0")
        return
    change = requested_amount % 10 
    amount = requested_amount - change
    change_user_balance(user_id, amount, False)
    if change > 0:
        print(f"Your change is {change} UAH")


def withdraw(user_id):
    try:
        amount = read_positive_num("Enter amount divisible by 10: ")
    except ValueError:
        print("Enter a number please")
        return
    except NegativeValueError:
        print("Your number should be bigger than 0")
        return
    if amount % 10 > 0:
        print("Not divisible by 10")
        return
    try:
        balance = get_balance(user_id)
    except UserNotFoundError as e:
        print(e)
        return
    if balance < amount:
        print("Your balance is less than requested amount")
        return
    tens, twenties, fifties, hundreds, two_hundreds, five_hundreds, thousands = get_atm_banknotes()
    total = calc_atm_balance(tens, twenties, fifties, hundreds, two_hundreds, five_hundreds, thousands)
    if total < amount:
        print("ATM balance is less than requested amount")
        return
    change_user_balance(user_id, amount, True)


def change_user_balance(user_id, amount, is_withdrawal):
    action = "deposit"
    if is_withdrawal:
        action = "withdraw"
        amount *= -1
    add_transaction(user_id, action, amount)
    cur.execute("""UPDATE users 
                   SET balance = balance + ? 
                   WHERE id = ?""", (amount, user_id))
    con.commit()


def read_positive_num(msg):
    num = read_num(msg)
    if num < 0:
        raise NegativeValueError(num)
    return num


def read_num(msg):
    return int(input(msg))


def user_menu(user_id):
    while True:
        print("--------------")
        print("To view the balance 1")
        print("To deposit enter 2")
        print("To withdraw enter 3")
        print("Exit 4")
        print("--------------")
        command = input("Enter your operation: ")
        if command == "1":
            view_balance(user_id)
        elif command == "2":
            deposit(user_id)
        elif command == "3":
            withdraw(user_id)
        elif command == "4":
            break
        else:
            print("Your command is not correct")


def start():
    create_tables()
    insert_tables()
    while True:
        print("--------------")
        print("Login 1\n"+
        "Register 2\n"+
        "Exit 3")
        print("--------------")
        command = input("Enter your command: ")
        if command == "1":
            username = input("Enter your name: ")
            password = input("Enter your password: ")
            try:
                user_id, is_incasator = login(username, password)  
                if is_incasator:
                    incasator_menu()
                else:
                    user_menu(user_id)
            except LoginError as e:
                print(e)
        elif command == "2":
            print("Your username length should be longer than 2 letters and shorter than 50 letters")
            print("and your password should have more than 8 symbols and have to contain at least 1 digit")
            username = input("Enter your name: ")
            password = input("Enter your password: ")
            if validate_registration(username, password):
                register(username, password)
        elif command == "3":
            break
        else:
            print("Your command is not correct")


if __name__ == "__main__":
    start()
