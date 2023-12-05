# 1. Додайте до банкомату меню отримання поточного курсу валют за допомогою requests 
# (можна використати відкрите API ПриватБанку)

import sqlite3
import random
import requests


class DataBase:
    def __init__(self, db_file):
        self.con = sqlite3.connect(db_file)
        self.cur = self.con.cursor()


    def create_tables(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            balance INTEGER NOT NULL DEFAULT 0,
            is_incasator BOOLEAN NOT NULL
        )""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            action TEXT NOT NULL, 
            amount INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS atm (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tens INTEGER NOT NULL DEFAULT 0,
            twenties INTEGER NOT NULL DEFAULT 0,
            fifties INTEGER NOT NULL DEFAULT 0,
            hundreds INTEGER NOT NULL DEFAULT 0,
            two_hundreds INTEGER NOT NULL DEFAULT 0,
            five_hundreds INTEGER NOT NULL DEFAULT 0,
            thousands INTEGER NOT NULL DEFAULT 0
        )""")
        self.con.commit()


    def insert_tables(self):
        self.cur.execute("""
            INSERT OR IGNORE INTO users(username, password, is_incasator) VALUES 
                ('Bob', '12345', FALSE),
                ('Alice', 'password', FALSE),
                ('Alex', '54321', FALSE),
                ('admin', 'admin', TRUE)
            """)

        self.cur.execute("""
            INSERT OR IGNORE INTO 
            atm(id, tens, twenties, fifties, hundreds, two_hundreds, five_hundreds, thousands) 
            VALUES (1, 20, 20, 20, 20, 20, 20, 20)
            """)
        self.con.commit()


db = DataBase("atm.db")


class ATM:
    def __init__(self, tens, twenties, fifties, hundreds, two_hundreds, five_hundreds, thousands):
        self.denominations = [1000, 500, 200, 100, 50, 20, 10]
        self.bills = {
            1000: thousands, 
            500: five_hundreds, 
            200: two_hundreds, 
            100: hundreds, 
            50: fifties, 
            20: twenties, 
            10: tens}


    def withdraw_bills(self, amount):
        combinations = self.generate_limited_combinations(amount, self.denominations, self.bills)
        best = self.calc_best_combination(combinations)
        if best is None:
            print("No bills")
            return False
        for denomination, count in best.items():
            self.bills[denomination] -= count
        self.save_atm()
        for denomination, count in best.items():
            print(f"{denomination} x {count}")
        return True


    def generate_limited_combinations(self, amount, denominations, limits, current_combination=None):
        if current_combination is None:
            current_combination = []
        if amount == 0:
            return [current_combination]

        combinations = []
        for i, denom in enumerate(denominations):
            if amount >= denom and limits[denom] > 0:
                remaining_denominations = denominations[i:]
                new_limits = limits.copy()
                new_limits[denom] -= 1
                combinations += self.generate_limited_combinations(amount - denom, remaining_denominations, new_limits, current_combination + [denom])

        return combinations


    def calc_best_combination(self, all_combinations):
        if len(all_combinations) == 0:
            return None
        best = all_combinations[0]
        for combination in all_combinations:
            if len(combination) < len(best):
                best = combination
        return {note: best.count(note) for note in set(best)}


    def format_combination(self, combination):
        return [f"{combination.count(denom)} x {denom}" for denom in set(combination)]


    def print_balance(self):
        for denomination, count in self.bills.items():
            print(f"{denomination}: {count}")
        total = self.calc_balance()
        print(f"Total balance: {total}")


    def calc_balance(self):
        return sum([denom * count for denom, count in self.bills.items()])


    def save_atm(self):
        db.cur.execute(f"""UPDATE atm SET
            thousands = ?,
            five_hundreds = ?,
            two_hundreds = ?,
            hundreds = ?,
            fifties = ?,
            twenties = ?,
            tens = ?""", (self.bills[1000], self.bills[500], self.bills[200], self.bills[100], self.bills[50],
            self.bills[20], self.bills[10]))
        db.con.commit()


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
            db.cur.execute(f"UPDATE atm SET {nominal_name} = ?", (amount,))
        db.con.commit()


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
        success = atm.withdraw_bills(amount)
        if success:
            self.change_balance(amount, True)


    def change_balance(self, amount, is_withdrawal):
        action = "deposit"
        if is_withdrawal:
            action = "withdraw"
            amount *= -1
        add_transaction(self.user_id, action, amount)
        db.cur.execute("""UPDATE users 
                    SET balance = balance + ? 
                    WHERE id = ?""", (amount, self.user_id))
        db.con.commit()


    def get_balance(self):
        db.cur.execute("""
        SELECT balance 
        FROM users WHERE id = ?""", (self.user_id, ))
        user_data = db.cur.fetchone()
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


def add_transaction(user_id, action, amount):
    db.cur.execute("""
    INSERT INTO transactions(user_id, action, amount) VALUES 
        (?, ?, ?)
    """, (user_id, action, amount))


def show_transactions(user_id):
    db.cur.execute("""
    SELECT action, amount 
    FROM transactions WHERE user_id = ?""", (user_id, ))
    transactions = db.cur.fetchall()
    for t in transactions:
        action, amount = t
        print(f"{action} : {amount} UAH")
    

def get_atm():
    db.cur.execute("""
    SELECT tens, twenties, fifties, hundreds, two_hundreds, five_hundreds, thousands 
    FROM atm WHERE id = 1""")
    tens, twenties, fifties, hundreds, two_hundreds, five_hundreds, thousands = db.cur.fetchone()
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
    db.cur.execute("""
    SELECT id, username, password, balance, is_incasator 
    FROM users WHERE username = ?""", (username, ))
    user_data = db.cur.fetchone()
    if not user_data:
        raise LoginError("User not found")
    user_id, username, password, balance, is_incasator = user_data
    if login_password != password:
        raise LoginError("Password incorrect")
    user = User(username, password, balance, user_id)
    return user, is_incasator


def register(username, password, bonus):
    db.cur.execute("""
    INSERT OR IGNORE INTO users(username, password, is_incasator, balance) VALUES 
        (?, ?, FALSE, ?)
    """, (username, password, bonus))
    db.con.commit()
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


def check_rates():
        url = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"
        try:
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Unexpected status code: {response.status_code}")
            data = response.json()
            print("Exchange Rates: ")
            for currency in data:
                print(f"{currency['ccy']}: {currency['buy']} / {currency['sale']}")
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")


def start():
    db.create_tables()
    db.insert_tables()
    atm = get_atm()
    while True:
        print("--------------")
        print("Login 1\n"+
        "Register 2\n"+
        "Check rates 3\n"+
        "Exit 4")
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
            check_rates()
        elif command == "4":
            break
        else:
            print("Your command is not correct")


if __name__ == "__main__":
    start()
