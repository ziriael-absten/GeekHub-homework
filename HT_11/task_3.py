# 3. Банкомат 2.0: переробіть программу з функціонального підходу програмування на використання 
# класів. Додайте шанс 10% отримати бонус на баланс при створенні нового користувача.


import sqlite3
import random


class ATM:
    def __init__(self, tens, twenties, fifties, hundreds, two_hundreds, five_hundreds, thousands):
        self.tens = tens
        self.twenties = twenties
        self.fifties = fifties
        self.hundreds = hundreds
        self.two_hundreds = two_hundreds
        self.five_hundreds = five_hundreds
        self.thousands = thousands


    def print_balance(self):
        print(f"10: {self.tens}")
        print(f"20: {self.twenties}")
        print(f"50: {self.fifties}")
        print(f"100: {self.hundreds}")
        print(f"200: {self.two_hundreds}")
        print(f"500: {self.five_hundreds}")
        print(f"1000: {self.thousands}")
        total = self.calc_balance()
        print(f"Total balance: {total}")


    def calc_balance(self):
        return self.tens * 10 + self.twenties * 20 + self.fifties * 50 + self.hundreds * 100 + \
        self.two_hundreds * 200 + self.five_hundreds * 500 + self.thousands * 1000


    def add_banknotes(self):
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


class User():
    def __init__(self, username, password, balance, user_id):
        self.username = username
        self.password = password
        self.balance = balance
        self.user_id = user_id


    def show_menu(self, atm):
        while True:
            print("--------------")
            print("To view the balance 1")
            print("To deposit enter 2")
            print("To withdraw enter 3")
            print("Exit 4")
            print("--------------")
            command = input("Enter your operation: ")
            if command == "1":
                self.view_balance()
            elif command == "2":
                self.deposit()
            elif command == "3":
                self.withdraw(atm)
            elif command == "4":
                break
            else:
                print("Your command is not correct")


    def view_balance(self):
        balance = self.get_balance()
        print(f"Your balance is {balance} UAH")


    def deposit(self):
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
        self.change_balance(amount, False)
        if change > 0:
            print(f"Your change is {change} UAH")


    def withdraw(self, atm):
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
            balance = self.get_balance()
        except UserNotFoundError as e:
            print(e)
            return
        if balance < amount:
            print("Your balance is less than requested amount")
            return
        atm_balance = atm.calc_balance()
        if atm_balance < amount:
            print("ATM balance is less than requested amount")
            return
        self.change_balance(amount, True)


    def change_balance(self, amount, is_withdrawal):
        action = "deposit"
        if is_withdrawal:
            action = "withdraw"
            amount *= -1
        add_transaction(self.user_id, action, amount)
        cur.execute("""UPDATE users 
                    SET balance = balance + ? 
                    WHERE id = ?""", (amount, self.user_id))
        con.commit()


    def get_balance(self):
        cur.execute("""
        SELECT balance 
        FROM users WHERE id = ?""", (self.user_id, ))
        user_data = cur.fetchone()
        if not user_data:
            raise UserNotFoundError("User not found")
        return user_data[0]


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
    

def get_atm():
    cur.execute("""
    SELECT tens, twenties, fifties, hundreds, two_hundreds, five_hundreds, thousands 
    FROM atm WHERE id = 1""")
    tens, twenties, fifties, hundreds, two_hundreds, five_hundreds, thousands = cur.fetchone()
    atm = ATM(tens, twenties, fifties, hundreds, two_hundreds, five_hundreds, thousands)
    return atm
    

nominal_names = {"10": "tens", "20": "twenties", "50": "fifties", "100": "hundreds",
 "200": "two_hundreds", "500": "five_hundreds", "1000": "thousands"}


def incasator_menu(atm):
    while True:
        print("--------------")
        print("To view the atm balance enter 1")
        print("To set banknotes enter 2")
        print("Exit 3")
        print("--------------")
        command = input("Enter your operation: ")
        if command == "1":
            atm.print_balance()
        elif command == "2":
            atm.add_banknotes()
            atm = get_atm()
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
    SELECT id, username, password, balance, is_incasator 
    FROM users WHERE username = ?""", (username, ))
    user_data = cur.fetchone()
    if not user_data:
        raise LoginError("User not found")
    user_id, username, password, balance, is_incasator = user_data
    if login_password != password:
        raise LoginError("Password incorrect")
    user = User(username, password, balance, user_id)
    return user, is_incasator


def register(username, password, bonus):
    cur.execute("""
    INSERT OR IGNORE INTO users(username, password, is_incasator, balance) VALUES 
        (?, ?, FALSE, ?)
    """, (username, password, bonus))
    con.commit()
    print("Registration successful")
    if bonus > 0:
        print(f"Congratulations, you won bonus {bonus} UAH")


def read_positive_num(msg):
    num = read_num(msg)
    if num < 0:
        raise NegativeValueError(num)
    return num


def read_num(msg):
    return int(input(msg))


def start():
    create_tables()
    insert_tables()
    atm = get_atm()
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
                user, is_incasator = login(username, password)  
                if is_incasator:
                    incasator_menu(atm)
                else:
                    user.show_menu(atm)
            except LoginError as e:
                print(e)
        elif command == "2":
            print("Your username length should be longer than 2 letters and shorter than 50 letters")
            print("and your password should have more than 8 symbols and have to contain at least 1 digit")
            username = input("Enter your name: ")
            password = input("Enter your password: ")
            if validate_registration(username, password):
                bonus = 0
                if random.random() < 0.1:
                    bonus = 50
                register(username, password, bonus)   
        elif command == "3":
            break
        else:
            print("Your command is not correct")


if __name__ == "__main__":
    start()
