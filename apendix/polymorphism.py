from abc import ABC, abstractmethod
 
class Figure(ABC):
 
    @abstractmethod
    def get_perimetr(self):
        pass

class Rect(Figure):
  def __init__(self, a, b):
    self.a = a
    self.b = b
  
  def get_perimetr(self):
    return 2 * (self.a + self.b)
  
class Sqare(Figure):
  def __init__(self, a):
    self.a = a
  
  def get_perimetr(self):
    return 4 * self.a
  
class Triangle(Figure):
  def __init__(self, a, b, c):
    self.a = a
    self.b = b
    self.c = c
  
  def get_perimetr(self):
    return self.a + self.b + self.c
  
  
r1 = Rect(1, 2)
r2 = Rect(3, 4)
s1 = Sqare(2)
s2 = Sqare(4)
t1 = Triangle(2, 3, 4)
t2 = Triangle(3, 4, 5)

figures = [r1, r2, s1, s2, t1, t2]

for fig in figures:
  print(fig.get_pr())  
  
