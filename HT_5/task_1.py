# task_1.py
# 
# Написати функцію , яка прийматиме один аргумент - сторону квадрата, і 
#  вертатиме 3 значення у вигляді кортежа: 
#  * периметр квадрата, площа квадрата, його діагональ
#  
import math
 

def characteristic_sqare(value):
    """
    Формування кортежу характеристик квадрада
    Периметр, Площа, Довжина діагоналі
    """
    return (4 * value, value * value, value * math.sqrt(2))

def remove_illegal_symbs(value):
    """
    Видалення із отриманого рядка вводу нечислових символів
    """
    templ = list(map(str, range(10)))
    templ.append(".")
    lst = []
    for item in value:
        if item in templ:
            lst.append(item)
    return "".join(lst)


if __name__ == "__main__":
    # Введення значення від користувача 
    for attempt in range(5):
        print(f"Attempt {attempt + 1}. ", end=" ")
        sinp = input("Enter side of sqare (number): ")
        value = None
        try:
            value = float(remove_illegal_symbs(sinp))
        except ValueError as ex:
            print(f"You enter wrong number: {sinp}")
            continue

        break
        
    # Обробка введеног значення
    if value:
        print(characteristic_sqare(value))
    else:
        print("You are not enter right value in 5 attempts.")

