# task_3.py
# Користувач вводить змінні "x" та "y" з довільними цифровими значеннями. 
# Створіть просту умовну конструкцію (звiсно вона повинна бути в тiлi ф-цiї), 
#  під час виконання якої буде перевірятися рівність змінних "x" та "y" та у 
#  випадку нерівності - виводити ще і різницю. 
# Повинні працювати такі умови (x, y, z заміність на відповідні числа): 
#  x > y; вiдповiдь - "х бiльше нiж у на z" 
#  x < y; вiдповiдь - "у бiльше нiж х на z" 
#  x == y. відповідь - "х дорівнює y"
#  

def get_user_input(msg="Please enter your value"):
    """
Getting user input 

return user input
    """
    return input(msg + ": ")

def isfloat(value):
    """
    Перевірка чи є рядок float числом
    повертає True чи False
    """
    try:
        float(value)
        return True
    except ValueError:
        return False

def try_convert_number(value):
    """
    Спроба провести приведення типу до числового int чи float
    Повертає число відповідного типу, або None якшо приведення не вдалося
    """
    result = None
    if isinstance(value, str):
        if isfloat(value):
            result = int(value) if value.isdigit() else float(value)
    elif isinstance(value, bool):
        return None
    elif isinstance(value, (int, float)):
        result = value
    return result

def baz(x, y):
    """
    Функція яку порібно зробити
    ---------------------------
    Функція перевірки рівності та нерівності параметрів
    Return: повідомлення про відношення змінних
    """
    if x == y:
        return F"{x} дорівнює {y}"
    elif x > y:
        return f"{x} бiльше нiж {y} на {x - y}"
    else:
        return f"{y} бiльше нiж {x} на {y - x}"

if __name__ == "__main__":
    x = try_convert_number(get_user_input("Enter number x").strip())
    y = try_convert_number(get_user_input("Enter number y").strip())
    if x is None:
        print("Error. You enter wrong number in x.")
        exit()
    if y is None:
        print("Error. You enter wrong number in y.")
        exit()
    print(baz(x, y))