# 2. Створіть за допомогою класів та продемонструйте свою реалізацію шкільної бібліотеки 
# (включіть фантазію). Наприклад вона може містити класи Person, Teacher, Student, Book, 
# Shelf, Author, Category і.т.д.

import json


class Shelf:
    def __init__(self):
        self.books = []


    def add_book(self, book):
        self.books.append(book)


    def __str__(self):
        return f"Books: {self.books}"


    def to_dict(self):
        return {"books": [book.to_dict() for book in self.books]}


class Book:
    def __init__(self, title, author, category):
        self.title = title
        self.author = author
        self.category = category
        self.is_borrowed = False
        self.borrower = None


    def to_dict(self):
        return {
            "title": self.title, 
            "author": self.author, 
            "category": self.category,
            "is_borrowed": self.is_borrowed,
            "borrower": self.borrower
            }


    def borrow(self, borrower):
        if not self.is_borrowed:
            self.is_borrowed = True
            self.borrower = borrower


    def return_book(self):
        if self.is_borrowed:
            self.is_borrowed = False
            self.borrower = None


    def __str__(self):
        status = "Available" if not self.is_borrowed else f"Borrowed by {self.borrower}"
        return f"Book: {self.title}, {self.author}, {self.category}, Status: {status}"


class Person:
    def __init__(self, name):
        self.borrowed_books = []
        self.name = name


    def borrow_book(self, book):
        self.borrowed_books.append(book.title)


    def return_book(self, book_title):
        if book_title in self.borrowed_books:
            self.borrowed_books.remove(book_title)
            print(f"{self.name} returned '{book_title}' successfully.")
        else:
            print(f"You don't have '{book_title}' borrowed.")


    def display_borrowed_books(self):
        if not self.borrowed_books:
            print("You haven't borrowed any books.")
        else:
            print("Books you have borrowed:")
            for book in self.borrowed_books:
                print(f"'{book}' borrowed from {self.name}")


    def to_dict(self):
        return {"name": self.name, "borrowed_books": self.borrowed_books}


def shelf_from_dict(data):
    books_data = data["books"]
    books = [book_from_dict(book) for book in books_data]
    shelf = Shelf()
    shelf.books = books
    return shelf


def book_from_dict(data):
    title = data["title"]
    category = data["category"]
    author = data["author"]
    is_borrowed = data["is_borrowed"]
    borrower = data["borrower"]
    book = Book(title, author, category)
    book.is_borrowed = is_borrowed
    book.borrower = borrower
    return book


def person_from_dict(data):
    person = Person(data["name"])
    person.borrowed_books = data["borrowed_books"]
    return person


class Library:
    def __init__(self):
        self.shelves = []
        self.persons = {}


    def store_library(self):
        library = {
            "shelves": [shelf.to_dict() for shelf in self.shelves],
            "persons": [person.to_dict() for person in self.persons.values()]
        }
        with open(f"library.json", 'w') as json_file:
            json.dump(library, json_file)


    def load_library(self):
        with open(f"library.json", 'r') as json_file:
            library_dict = json.load(json_file)
            self.shelves = [shelf_from_dict(shelf_dict) for shelf_dict in library_dict["shelves"]]
            self.persons = {persons_dict["name"]: person_from_dict(persons_dict) for persons_dict in library_dict["persons"]}


    def add_shelf(self, shelf):
        self.shelves.append(shelf)


    def add_person(self, name):
        self.persons[name] = Person(name)


    def display_books(self):
        print("Library Inventory:")
        for i, shelf in enumerate(self.shelves, 1):
            print(f"Shelf {i}: {shelf}")


    def borrow_book(self, book_title, borrower_name):
        for shelf in self.shelves:
            for book in shelf.books:
                if book.title == book_title and not book.is_borrowed:
                    book.borrow(borrower_name)
                    self.persons[borrower_name].borrow_book(book)
                    print(f"{borrower_name} borrowed '{book.title}' successfully.")
                    self.store_library()
                    return
        print(f"Sorry, '{book_title}' is not available for borrowing.")


    def return_book(self, book_title, borrower_name):
        if borrower_name in self.persons:
            self.persons[borrower_name].return_book(book_title)
            for shelf in self.shelves:
                for book in shelf.books:
                    if book.title == book_title:
                        book.return_book()
            self.store_library()
        else:
            print(f"Invalid attempt to return '{book_title}'. Person '{borrower_name}' not found.")


    def display_borrowed_books(self, borrower_name):
        if borrower_name in self.persons:
            self.persons[borrower_name].display_borrowed_books()
        else:
            print(f"Person '{borrower_name}' not found.")


def init_data():
    library = Library()
    shelf1 = Shelf()
    shelf2 = Shelf()
    library.add_shelf(shelf1)
    library.add_shelf(shelf2)

    author_jk_rowling = "J.K. Rowling"
    author_jd_salinger = "J.D. Salinger"
    author_john_smith = "John Smith"

    category_fiction = "Fiction"
    category_programming = "Programming"

    book1 = Book("Harry Potter", author_jk_rowling, category_fiction)
    book2 = Book("The Catcher in the Rye", author_jd_salinger, category_fiction)
    book3 = Book("Python Programming", author_john_smith, category_programming)

    shelf1.add_book(book1)
    shelf1.add_book(book2)
    shelf2.add_book(book3)


def start():
    library = Library()
    library.load_library()

    while True:
        print("1. Display Library Inventory")
        print("2. Borrow a Book")
        print("3. Return a Book")
        print("4. Display Borrowed Books")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")
        if choice == "1":
            library.display_books()
        elif choice == "2":
            borrower_name = input("Enter your name: ")
            if borrower_name not in library.persons:
                library.add_person(borrower_name)
            book_title = input("Enter the title of the book you want to borrow: ")
            library.borrow_book(book_title, borrower_name)
        elif choice == "3":
            borrower_name = input("Enter your name: ")
            book_title = input("Enter the title of the book you want to return: ")
            library.return_book(book_title, borrower_name)
        elif choice == "4":
            borrower_name = input("Enter your name: ")
            library.display_borrowed_books(borrower_name)
        elif choice == "5":
            print("Exiting the library. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


start()
