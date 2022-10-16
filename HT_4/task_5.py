# task_5.py
# Калькулятор 
# Повинна бути 1 функцiя, яка приймає 3 аргументи - один з яких операцiя, 
#  яку зробити! 
# Аргументи брати від юзера (можна по одному - окремо 2, окремо +, окремо 2; 
# можна всі разом - типу 2 + 2). 
# Операції що мають бути присутні: +, -, *, /, %, //, **. 
# Не забудьте протестувати з різними значеннями на предмет помилок!
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


def my_add(left_op, right_op):
    """
    Функція що проводить операцію додавання
    Попертає результат arg1 + arg2
    """
    return left_op + right_op

def my_sub(left_op, right_op):
    """
    Функція що проводить операцію віднімання
    Попертає результат arg1 - arg2
    """
    return left_op - right_op

def my_mul(left_op, right_op):
    """
    Функція що проводить операцію множення
    Попертає результат arg1 * arg2
    """
    return left_op * right_op

def my_truediv(left_op, right_op):
    """
    Функція що проводить операцію ділення
    Попертає результат arg1 / arg2
    """
    return left_op / right_op

def my_floordiv(left_op, right_op):
    """
    Функція що проводить операцію цілочисленного ділення
    Попертає результат arg1 // arg2
    """
    return left_op // right_op


def my_mod(left_op, right_op):
    """
    Функція що проводить операцію визначення остачі від ділення
    Попертає результат arg1 // arg2
    """
    return left_op % right_op

def my_pow(left_op, right_op):
    """
    Функція що проводить операцію піднесення у степінь
    Попертає результат arg1 ** arg2
    """
    return left_op ** right_op


def calculator():
    """
    Функція калькулятор
    """

    operations = {"+":my_add, "-":my_sub, "*":my_mul, "/":my_truediv, "//":my_floordiv, "%":my_mod, "**":my_pow}  
    reg_1 = None
    reg_2 = None
    op = ""

    while True:
        reg_1 = try_convert_number(get_user_input("Enter first value").strip())
        if reg_1 is None:
            continue
        else:
            break

    while True:
        op = get_user_input("Enter operation one of (+,-,*,/,//,%,**)").strip()
        if op not in operations.keys():
            continue
        else:
            break


    while True:
        reg_2 = try_convert_number(get_user_input("Enter second value").strip())
        if reg_2 is None:
            continue
        else:
            break

    result = operations[op](reg_1, reg_2)
    print(f"Result: {result}")
    return result


if __name__ == "__main__":
    calculator()
        
