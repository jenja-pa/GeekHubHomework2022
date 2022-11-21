# task_2.py
# 2. [ ] Створіть за допомогою класів та продемонструйте свою реалізацію 
# шкільної бібліотеки (включіть фантазію). 
# Наприклад вона може містити класи:
#   Person, Teacher, Student, Book, Shelf, Author, Category і.т.д. 
# Можна робити по прикладу банкомату з меню, базою даних і т.д.
import os
import json


class Library:
    """
    Клас, що відповідає за реалізацію роботи бібліотеки
    реалізує патерн Singleton
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, address, name, f_name="library.json"):
        self.address = address
        self.name = name
        self.f_name = f_name
        self.persons = []
        self.storage = Vault()

    def __str__(self):
        return f"Бібліотека адреса:{self.address}, "\
               f"назва: {self.name} {os.linesep}"\
               f"Книжок у сховищі: {sum(self.storage.dct_books().values())}, "\
               f"видано: {sum(self.dct_persons_books().values())}"

    def __repr__(self):
        return f"Library('{self.address}', '{self.name}')"

    def append_books(self, book, cnt):
        """Додати книгу в сховище вказану кількаість разів"""
        for _ in range(cnt):
            self.storage.append(book)

    def dump(self):
        """Збереження стану бібліотеки у файл"""
        with open(self.f_name, "w", encoding="utf-8") as f:
            # books in storage
            tpl_storage = self.storage.prepare_data()
            lst_persons = [person.prepare_data() for person in self.persons]
            
            dct_dump = {
                "name": self.name,
                "address": self.address,
                "persons": lst_persons,
                "storage": tpl_storage
            }

            json.dump(dct_dump, f, indent=4)

    def load(self):
        """ Відновлення стану бібліотеки із файла """
        self.storage.books.clear()
        self.persons.clear()
        with open(self.f_name, encoding="utf-8") as f:
            data = json.load(f)
        self.storage.unpack_data(data["storage"])
        for json_person in data["persons"]:
            if json_person["role"] == "Teacher":
                person = Teacher(json_person["name"], int(json_person["age"]))
            else:
                person = Student(json_person["name"], int(json_person["age"]))
            person.unpack_data_books(json_person["books"], person)
            self.append_person(person)

    def show_persons(self):
        """Перелік наявних користувачів"""
        for person in self.persons:
            person.show()

    def dct_persons_books(self):
        dct = {}
        for person in self.persons:
            for book in person.books:
                dct[book.show_info()] = dct.get(book.show_info(), 0) + 1
        return dct        

    def seq_persons_books(self):
        """Передік книг які видані"""
        return (
            f"{book} : {cnt} avialible" 
            for book, cnt in self.dct_persons_books().items())
    
    def show_persons_books(self):
        """Вивід книг які були видані"""
        for item in self.seq_persons_books():
            print(item)

    # def show_person_books(self, person):
    #     """Перелік книг у читача"""
    #     f_person = self.find_person(person)
    #     if f_person:
    #         f_person.show()

    def give_book_to_person(self, person, book):
        """Пидати книгу читачу"""
        f_person = None
        try:
            f_person = self.find_person(person)
        except KeyError:
            print(f"На жаль користувач {f_person} - не існує")
            return

        f_book = None
        try:
            f_book = self.storage.find(book)
        except KeyError:
            print(f"На жаль книга {f_book} - відсутня у сховищі")
            return

        f_person.append_book(book)
        self.storage.take(f_book)

    def return_book_to_storage(self, person, book):
        """Повернути книгу в бібліотеку"""
        f_person = None
        try:
            f_person = self.find_person(person)
        except KeyError:
            print(f"На жаль користувач {f_person} - не існує")
            return

        f_book = None
        try:
            f_book = f_person.find_book(book)
        except KeyError:
            print(f"На жаль книга {f_book} - відсутня у користувача " 
                  f"{str(person)}")
            return

        self.storage.append(f_book)    
        f_person.books.remove(f_book)        

    def show_avialible_books(self):
        """Передік книг які наявні у бібліотеці (виданих та присутніх)"""
        dct = {}
        dct_p = self.dct_persons_books()
        dct_s = self.storage.dct_books()
        keys = set(dct_p.keys()).union(dct_s.keys())
        for key in keys:
            dct[key] = dct_p.get(key, 0) + dct_s.get(key, 0)

        print("All books in library on hand and in storage are:")
        for book_info in dct:
            print(f"{book_info} : {dct[book_info]} avialible")

    def show_storage_books(self):
        """Dbdsl Переkікe книг які наявні у сховищі]"""
        self.storage.show()

    def find_person(self, p_person):
        """Пошук читача у списку читачів"""
        for person in self.persons:
            if str(person) == str(p_person):
                return person

    def append_person(self, person):
        f_person = self.find_person(person)
        if f_person:
            print(f"На жаль такий користувач {person} вже присутній")
        else:
            self.persons.append(person)


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.books = []

    def __str__(self):
        return f"Person: (name={self.name}, age={self.age})"

    def __repr__(self):
        return f"Person({self.name}, {self.age})"

    def find_book(self, p_book):
        for book in self.books:
            if str(book) == str(p_book):
                return book
        return None

    def append_book(self, book):
        self.books.append(book)

    def remove_book(self, book):
        self.books.remove(book)

    def show(self):
        raise NotImplementedError("You neer to replace method .show()")

    def show_books(self):
        print(f"Наявні книги: {len(self.books)} у читача")
        for book in self.books:
            print(book.show_info())

    def prepare_data(self):
        """ Підготовка Person до серіалізації """
        return {
            "name": self.name,
            "age": self.age,
            "books": [repr(book) for book in self.books]
            }
    
    def unpack_data_books(self, data, person):
        """ Відновлення об'єктів Book для person із текстового вигдяду """
        if data:
            for repr_book in data["books"]:
                book = Book.create_from_repr(repr_book)
                person.append_book(book)


class Teacher(Person):
    def __init__(self, name, age):
        super().__init__(name, age)

    def __str__(self):
        return f"Teacher: name={self.name}, age={self.age}"

    def __repr__(self):
        return f"Teacher({self.name}, {self.age})"

    def show(self):
        print(f"Учитель {self.name}, {self.age} років")
        super().show_books()

    def prepare_data(self):
        dct = super().prepare_data()
        dct["role"] = "Teacher"
        return dct

    @staticmethod
    def input():
        print("Please input Teacher info:")
        return Teacher(
            input("name: "), 
            input("age: ") 
            )


class Student(Person):
    def __init__(self, name, age):
        super().__init__(name, age)
        self.books = []

    def __str__(self):
        return f"Student: name={self.name}, age={self.age}"

    def __repr__(self):
        return f"Student({self.name}, {self.age})"

    def show(self):
        print(f"Студент {self.name}, {self.age} років")
        super().show_books()

    def prepare_data(self):
        dct = super().prepare_data()
        dct["role"] = "Student"
        return dct

    @staticmethod
    def input():
        print("Please input Student info:")
        return Student(
            input("name: "), 
            input("age: ") 
            )


class Book:
    """Класс, що описує книгу"""
    def __init__(self, author, name, category, language, pages):
        self.author = author
        self.name = name
        self.category = category
        self.language = language
        self.pages = pages

    def key(self):
        return (self.author, self.name, self.category, self.language, 
                self.pages)

    def __str__(self):
        return f"book: {self.author}-{self.name}-{self.category}-" \
               f"{self.language}-{self.pages}"

    def __repr__(self):
        return f"Book('{self.author}', '{self.name}', '{self.category}', " \
               f"'{self.language}', '{self.pages}')"

    def show_info(self):
        return f"{self.author}, {self.name}, {self.category}, " \
               f"{self.language}, {self.pages}"

    @staticmethod
    def input():
        print("Input book parameters:")
        return Book(
            input("Author: "), 
            input("Name: "), 
            input("Categogy: "), 
            input("Language: "), 
            input("Cnt pages: "), 
            )

    @staticmethod
    def create_from_repr(repr_book):
        str_book = repr_book[:-1].replace("Book(", "").replace(", ", "|")
        tpl_book = tuple(item.strip("'") for item in str_book.split("|"))
        return Book(*tpl_book)


class Vault:
    """Сховище книг бібліотеки"""
    def __init__(self):
        self.books = []

    def __str__(self):
        return f"This is Library storage has {len(self.books)} books"

    def __repr__(self):
        return "Vault()"

    def find(self, f_book):
        """Знайти книгу в сховиші"""
        for book in self.books:
            if str(book) == str(f_book):
                return book
        return None

    def append(self, book):
        """Додпти книгу в сховище"""
        self.books.append(book)

    def take(self, t_book):
        """Взяти книгу зі сховища"""
        find_book = self.find(t_book)
        if find_book:
            self.books.remove(find_book)
            return find_book
        raise KeyError(f"Exception book:{str(t_book)} does not found " 
                       f"in storage.")

    def show(self):
        """Вивід переліку книг у сховищі"""
        print("Книги у сховищі:")
        for book_info in self.seq_books():
            print(book_info)

    def dct_books(self):
        dct = {}
        for book in self.books:
            dct[book.show_info()] = dct.get(book.show_info(), 0) + 1
        return dct

    def seq_books(self):
        dct = self.dct_books()
        return (f"{book} : {cnt} шт." for book, cnt in dct.items())

    def prepare_data(self):
        """Підготовка даних сховища у формат зручний до збереження в json"""
        return tuple(repr(book) for book in self.books)

    def save_json(self, f_name):
        """Збереження книг присутніх у сховищі"""
        with open(f_name, "w", encoding="utf-8") as f:
            tpl = self.prepare_data()
            json.dump(tpl, f, indent=4)
    
    def unpack_data(self, data):
        """Розпаковка отриманих із json даних"""
        for repr_book in data:
            self.books.append(Book.create_from_repr(repr_book))

    def load_json(self, f_name):
        """Завантаження раніще збережених книг у сховище"""
        self.books.clear()
        with open(f_name, encoding="utf-8") as f:
            vault = json.load(f)
            self.unpack_data(vault)


if __name__ == "__main__":
    print("--Створення бібліотеки")
    lib = Library("м.Черкаси, вул. Степана Гмирі, 35", 
                  "Комунальна бібліотека №2")
    print(lib)
    print(f"{lib=}")

    print("--Створення другого екземпляра бібліотеки")
    lib2 = Library("м.Черкаси, вул. Остафія Дашковича, 17", 
                   "Міська бібліотека №1")
    print(lib2)
    print(f"{lib2=}")

    print("--Порівняння екземплярів бібліотеки")
    print(f"{id(lib)} == {id(lib2)} -> {id(lib) == id(lib2)}")

    print("--Додаємо книги до сховища")
    lib.append_books(Book(
        'Daniel Defo', 'Robinson Cruzo', 'Sea', 'En', '458'), 10)
    lib.append_books(Book(
        'Юрій Когут', 
        'Кібербезпека та ризики цифрової трансформації компаній', 
        'computer', 'Ua', '372'), 5)
    lib.append_books(Book(
        'Uri Kogut', 
        'Cybersequrity and risk digital transformation', 
        'computer', 'En', '372'), 1)
    lib.append_books(Book(
        'Олексій Васильєв', 'Алгоритми', 'computer', 'Ua', '424'), 3)
    lib.append_books(Book(
        'Toni Farel', 
        'Build. An Unorthodox Guide to Making Things Worth Making', 
        'selfbuilding', 'Ua', '1464'), 2)
    lib.storage.show()

    print("--Додаємо Користувачів")
    t = Teacher("Урманська Катерина Павлівна", "48")
    lib.append_person(t)
    t.show()
    st = Student("Мірошник Анатолій Сергійович", "19")
    lib.append_person(st)
    st.show()

    print("--Інтерактивно Додаємо Користувачів")
    # print("---Користувач Учитель:")
    # lib.append_person(Teacher.input())
    print("---Користувач Студент:")
    st2 = Student.input()
    lib.append_person(st2)
    st2.show()

    print("--Доступні Користувачі:")
    lib.show_persons()
    
    print("--Видати Користувачу книгу: яка існує")
    book = Book('Daniel Defo', 'Robinson Cruzo', 'Sea', 'En', '458')
    st_t = lib.find_person(st)
    lib.give_book_to_person(st_t, book)
    book = Book(
        'Uri Kogut', 
        'Cybersequrity and risk digital transformation', 
        'computer', 'En', '372')
    lib.give_book_to_person(st_t, book)
    st_t.show()

    print("--Список усіх наявних книг")
    lib.show_avialible_books()
    print("--Список усіх доступних книг(у сховищі)")
    lib.show_storage_books()
    print("--Список книг у читачів")
    lib.show_persons_books()

    print("--Користувачу здає книгу: яка існує")
    book = Book('Daniel Defo', 'Robinson Cruzo', 'Sea', 'En', '458')
    lib.return_book_to_storage(st_t, book)
    st_t.show()

    # print("--Збереження стану")
    # lib.dump()

    # print("--Відновлення стану")
    # lib.load()
    # lib.show_persons()
