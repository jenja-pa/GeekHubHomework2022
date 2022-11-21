# task_2.py
# 2. [ ] Створіть за допомогою класів та продемонструйте свою реалізацію 
# шкільної бібліотеки (включіть фантазію). 
# Наприклад вона може містити класи:
#   Person, Teacher, Student, Book, Shelf, Author, Category і.т.д. 
# Можна робити по прикладу банкомату з меню, базою даних і т.д.
import os


class Library:
    """
    Клас, що відповідає за реалізацію роботи бібліотеки
    реалізує патерн Singleton
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__init__()
        return cls.__instance

    def __init__(self, address):
        self.address = address
        # list (Book, cnt_present)
        self.books = []
        self.persons = []
        self.shelfs = []

    def add_book(self, book, cnt):
        if self.find_book(book):
            self.set_change_cnt_book(book, cnt)
        else:
            self.books.append(book, cnt)

    def show_avialible_books(self):
        """Передік книг які наявні у бібліотеці (виданих та присутніх)"""
        return (item[0] for item in self.books)

    def present_books(self):
        """Передік книг які присутні(готові до видачі) у бібліотеці (присутніх)"""
        return (item[0] for item in self.books if item[1] > 0)

    def find_book(self, book):
        """Пошук книги в переліку наявних книг"""
        return tuple(filter(lambda item: item[0].key==book.key, self.books))


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.books = []

    def __str__(self):
        return f"Person: (name={self.name}, age={self.age})"

    def __repr__(self):
        return f"Person({self.name}, {self.age})"


class Teacher(Person):
    def __init__(self, name, age):
        super().init(name, age)

    def __str__(self):
        return f"Teacher: name={self.name}, age={self.age}"

    def __repr__(self):
        return f"Teacher({self.name}, {self.age})"

    @staticmethod
    def input():
        print("Please input Teacher info:")
        return Author(
            input("name: "), 
            input("age: ") 
            )


class Student(Person):
    def __init__(self, name, age):
        super().init(name, age)

    def __str__(self):
        return f"Student: name={self.name}, age={self.age}"

    def __repr__(self):
        return f"Student({self.name}, {self.age})"

    @staticmethod
    def input():
        print("Please input Student info:")
        return Author(
            input("name: "), 
            input("age: ") 
            )


class Author(Person):
    def __init__(self, name, age):
        super().init(name, age)

    def __str__(self):
        return f"Author: name={self.name}, age={self.age}"

    def __repr__(self):
        return f"Author({self.name}, {self.age})"

    @staticmethod
    def input():
        print("Please input Author info:")
        return Author(
            input("name: "), 
            input("age: ") 
            )


class Book:
    """Класс, що описує книгу"""
    def __init__(self, author, category, language, pages):
        self.author = author
        self.category = category
        self.language = language
        self.pages = pages

    def key(self):
        return f"{self.author}-{self.category}-{self.language}-{self.pages}"

    def __str__(self):
        self.key()

    def __repr__(self):
        return f"Book('{self.author}', '{self.category}', '{self.language}', '{self.pages}')"

    @staticmethod
    def input():
        return Book(
            input("Input Author of book: "), 
            input("Input Categogy of book: "), 
            input("Input Language of book: "), 
            input("Input Count of pages book: "), 
            )


class Shelver:
    """Модель стелажа в бібліотеці"""
    __cnt = 0

    def __new__(cls, *args, **kwargs):
        Shelver.__cnt += 1
        return super().__new__(cls)

    def __init__(self, cnt_of_shelfs=10, amounth_shelf=30):
        """Модель стелажа для зберігання книг у бібліотеці"""
        self.num = Shelver.__cnt - 1
        self.cnt_of_shelfs = cnt_of_shelfs
        self.amounth_shelf = amounth_shelf
        self.shelfs = []
        # Створюємо визначену параметрами структуру для зберігання книжок
        for idx in range(self.cnt_of_shelfs):
            self.shelfs.append(Shelf(idx, self.amounth_shelf))

    def __str__(self):
        s = f"Shelver[#{self.num}, cnt shelfs:{len(self.shelfs)}]"
        lst = [s]
        for idx, shelf in enumerate(self.shelfs):
            lst.append(f"({idx}) shelf - present: {len(shelf.books)} books of {self.amounth_shelf}")

        return os.linesep.join(lst)

    def __repr__(self):
        return f"Shelver({self.cnt_of_shelfs}, {self.amounth_shelf})"

    def find(self, book):
        result_find = [shelf.find(book) for shelf in self.shelfs]
        if any(map(lambda item: item[1],result_find)):
            find_shelf = tuple(filter(lambda item: item[1], result_find))[0]
            return (self.num - 1, find_shelf, book)
        return None


class Shelf:
    """Інформація про полицю стелажа бібліотеки де розміщені книги"""
    def __init__(self, idx, amounth_shelf=30):
        self.idx = idx
        self.amounth_shelf = amounth_shelf
        self.books = []

    def find(self, book):
        for idx, sh_book in enumerate(self.books):
            if str(sh_book) == str(book):
                return (idx, sh_book)
        return None

    def append(self, book):
        """Покласти книгу на полицю"""
        if len(self.books) < self.amounth_shelf:
            self.books.append(book)
        else:
            raise KeyError(f"book: {book.author}-{book.name} do not able to append into shelf, she is full")

    def remove(self, book):
        """Забрати книгу з полиці"""
        result_find = self.find(book)
        if result_find:
            return self.books.pop(result_find[0])
        raise KeyError(f"book: {book.author}-{book.name} do not able to remove from shelf.")

    def show(self):
        print(f"Books avialible on shelf: {self.idx}")
        for book in self.books:
            print(str(book))

    def __str__(self):
        return f"({self.idx}) shelf - present: {len(self.books)} books"

    def __repr__(self):
        return f"Shelf({self.idx}, {self.amounth_shelf})"


class Category:
    pass


if __name__ == "__main__":
    sh = Shelver(2, 5)
    print(sh)
    print(sh.shelfs)