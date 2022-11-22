# task_1.py
# 1. Напишіть програму, де клас «геометричні фігури» (Figure) містить 
# властивість color з початковим значенням white і метод для зміни 
# кольору фігури, а його підкласи 
# «овал» (Oval) і «квадрат» (Square) 
# містять методи _init_ для завдання початкових розмірів об'єктів при 
# їх створенні.

class Figure:
    color = "White"

    @classmethod
    def set_color(cls, color):
        print(f"set_color: {cls}")
        cls.color = color
  
    def __str__(self):
        return f"This is Figure() cls.color={self.color})"

    def __repr__(self):
        return "Figure()"


class Oval(Figure):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height

    def __str__(self):
        return f"This is Oval (width={self.width}, height={self.height}, "\
               f"color={self.color})"

    def __repr__(self):
        return f"Oval({self.width}, {self.height})"


class Square(Figure):
    def __init__(self, a):
        super().__init__()
        self.width = a
        self.height = a

    def __str__(self):
        return f"This is Square (width={self.width}, height={self.height}, "\
               f"color={self.color})"

    def __repr__(self):
        return f"Square({self.width}, {self.height})"


print("Create Figure")
f1 = Figure()
print(f"{str(f1)}")
print("Figure change color to Green")
f2 = Figure()
f2.set_color("Green")
print(f"{str(f2)}")
print()

print("Create Oval o1")
o1 = Oval(23, 45)
print(f"o1={str(o1)}")
print("Change color: to Red")
o1.set_color("Red")
print(f"o1={str(o1)}")
print("Create Another Oval o2, color steel Red")
o2 = Oval(2, 4)
print(f"o2={str(o2)}")
print()

print("Create Square s1")
s1 = Square(12)
print(f"s1={str(s1)}")
print("Change color: to Blue")
s1.set_color("Blue")
print(f"s1={str(s1)}")
print("Create Another Square s2")
s2 = Square(2)
print(f"s2={str(s2)}")
