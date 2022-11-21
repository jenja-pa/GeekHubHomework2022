# task_1.py
# 1. Напишіть програму, де клас «геометричні фігури» (Figure) містить 
# властивість color з початковим значенням white і метод для зміни 
# кольору фігури, а його підкласи 
# «овал» (Oval) і «квадрат» (Square) 
# містять методи _init_ для завдання початкових розмірів об'єктів при 
# їх створенні.

class Figure:
    def __init__(self, color="White"):
        self.color = color

    def set_color(self, color):
        self.color = color
  
    def __str__(self):
        return f"This is Figure(color={self.color})"

    def __repr__(self):
        return f"Figure(color={self.color})"


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


print("Figure")
f1 = Figure()
print(f"{f1=}")
print("Figure Green")
f2 = Figure("Green")
print(f"{f2=}")

print()
o1 = Oval(23, 45)
print(o1)
print("Change color: to Red")
o1.set_color("Red")
print(o1)
print(f"{o1=}")

print()
s1 = Square(12)
print(f"{s1=}")
print("Change color: to Blue")
s1.set_color("Blue")
print(s1)
print(f"{s1=}")
