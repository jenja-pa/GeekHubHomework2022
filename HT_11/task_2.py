# task_2.py
# 2. [X] Створити клас Person, в якому буде присутнім метод __init__ який 
# буде приймати якісь аргументи, які зберігатиме в відповідні змінні.
#   - [X] Методи, які повинні бути в класі Person 
#         - show_age, print_name, show_all_information.
#   - [X] Створіть 2 екземпляри класу Person та в кожному з екземплярів 
# створіть атрибут profession (його не має інсувати під час ініціалізації в 
# самому класі) та виведіть його на екран (прінтоніть)
class Person:
    """
    Клас що поводить роботу із набором даних Особистість


    Attributes
    ----------
    name : str
        Ім'я особистості
    age : int
        Вік особистості

    Methods
    -------
    show_age()
        Виводить форматоване повідомлення про вік
    print_name()
        Виводить форматоване повідомлення про ім'я
    show_all_information()
        Виводить форматоване повідомлення: повна інформація по особистості
    """

    def __init__(self, name, age):
        self.name = name 
        self.age = age

    def show_age(self):
        print(f"Your have {self.age} years old.")

    def print_name(self):
        print(f"Your name is {self.name}.")

    def show_all_information(self):
        self.print_name()
        self.show_age()


if __name__ == "__main__":
    person1 = Person("Alex", 34)
    person2 = Person("Migel", 21)

    person1.profession = "CEO"
    person2.profession = "designer"

    print("person1")
    person1.show_all_information()
    print(f"Your profession is {person1.profession}")

    print()
    print("person2")
    person2.show_all_information()
    print(f"Your profession is {person2.profession}")
