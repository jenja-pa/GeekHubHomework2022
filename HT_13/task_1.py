# task_1.py
# 1. [ ] Створіть клас Car, який буде мати властивість year (рік випуску). 
#  Додайте всі необхідні методи до класу, щоб можна було виконувати порівняння 
# car1 > car2, яке буде показувати, що car1 старша за car2.
#  Також, операція car1 - car2 повинна повернути різницю між роками випуску. 
from functools import total_ordering


@total_ordering
class Car:
    def __init__(self, year: int, description: str):
        self.year = year 
        self.description = description

    @property
    def year(self):
        return self._year
    
    @year.setter
    def year(self, value):
        self._year = value

    def __sub__(self, other):
        if not isinstance(other, Car):
            raise TypeError(f"Another object must be a type of {self.__class__}")
        return abs(self.year - other.year)

    def __str__(self):
        return f"Car {self.description} of {self.year} year made"

    def __eq__(self, other):
        return self.year == other.year

    def __lt__(self, other):
        return not self.year < other.year


if __name__ == "__main__":
    car1 = Car(1978, "Ford Mustang")
    car2 = Car(2006, "Mersedes Q5")
    print(f"{str(car1)=}\n{str(car2)=}")
    
    print()
    print("car1 == car2", car1 == car2)
    print("car1 > car2", car1 > car2)
    print("car1 < car2", car1 < car2)
    print("car1 >= car2", car1 >= car2)
    print("car1 <= car2", car1 <= car2)

    print()
    obj = []
    print("car1 - car2", car1 - car2, "year of difference")
    
    print(car1.__class__)
    print()
    try:
        print("Try Wromg operation: car1:Car - obj:list -> Exception")
        print(car1 - obj)
    except TypeError as ex:
        print("Raised Exception:", ex)
