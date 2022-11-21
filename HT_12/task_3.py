# task_3.py
# 3. [ ] Створіть клас в якому буде атрибут який буде рахувати кількість 
# створених екземплярів класів.

class Person:
    
    __cnt_instances = 0

    def __new__(cls, *args, **kwargs):
        cls.__cnt_instances += 1
        return super().__new__(cls)

    def __del__(self):
        Person.__cnt_instances -= 1

    def __init__(self, name, surname, patronimic):
        self.name = name
        self.surname = surname
        self.patronimic = patronimic

    def __repr__(self):
        return f"Person ({self.name}, {self.surname}, {self.patronimic}) count of instances: {Person.__cnt_instances}"


p1 = Person("Alex", "Nx", "Parone")
print(p1)
p1.__cnt_instances = 100
p2 = Person("Josh", "Gard", "Beloweser")
print(p2)
p3 = Person("Kurt", "Denmot", "Elenwar")
print(p3)

print(p1, p2, p3)

p3 = None
print(p1)
