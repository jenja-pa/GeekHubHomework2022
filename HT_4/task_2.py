# task_2.py
# Створіть 3 рiзних функцiї (на ваш вибiр). 
# Кожна з цих функцiй повинна повертати якийсь результат (напр. інпут 
#  від юзера, результат математичної операції тощо). 
# Також створiть четверту ф-цiю, яка всередині викликає 3 попередні, 
#  обробляє їх результат та також повертає результат своєї роботи. 
# Таким чином ми будемо викликати одну (четверту) функцiю, а вона в 
#  своєму тiлi - ще 3.
# 
import operator as op

 
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


def test_operands(left_op, right_op):
    """
    Тестуємо тип переданих операндів на числове значення
    Повертається True чи False, та виводиться повідомлення про помилку
    """
    try:
        if not isinstance(left_op, (float, int)):
            raise TypeError("ErrorMessage: par left_operand must be a number.")
        if not isinstance(right_op, (float, int)):
            raise TypeError("ErrorMessage: par right_operand must be a number.")
    except TypeError as ex:
        print(ex)
        return False
    return True

def my_add(left_op, right_op):
    """
    Функція що проводить операцію додавання
    Попертає результат arg1 + arg2, або None якщо якийсь операнд не число
    """
    if test_operands(left_op, right_op):
        return left_op + right_op
    return None

def my_sub(left_op, right_op):
    """
    Функція що проводить операцію віднімання
    Попертає результат arg1 - arg2, або None якщо якийсь операнд не число
    """
    if test_operands(left_op, right_op):
        return left_op - right_op
    return None

def my_mul(left_op, right_op):
    """
    Функція що проводить операцію множення
    Попертає результат arg1 * arg2, або None якщо якийсь операнд не число
    """
    if test_operands(left_op, right_op):
        return left_op * right_op
    return None

def my_truediv(left_op, right_op):
    """
    Функція що проводить операцію ділення
    Попертає результат arg1 / arg2, або None якщо якийсь операнд не число
    """
    if test_operands(left_op, right_op):
        return left_op / right_op
    return None

def my_floordiv(left_op, right_op):
    """
    Функція що проводить операцію цілочисленного ділення
    Попертає результат arg1 // arg2, або None якщо якийсь операнд не число
    """
    if test_operands(left_op, right_op):
        return left_op // right_op
    return None


def my_mod(left_op, right_op):
    """
    Функція що проводить операцію визначення остачі від ділення
    Попертає результат arg1 // arg2, або None якщо якийсь операнд не число
    """
    if test_operands(left_op, right_op):
        return left_op % right_op
    return None

def my_pow(left_op, right_op):
    """
    Функція що проводить операцію піднесення у степінь
    Попертає результат arg1 ** arg2, або None якщо якийсь операнд не число
    """
    if test_operands(left_op, right_op):
        return left_op ** right_op
    return None

def boo():
    """
    Функція, що проводить визов інщих функцій
    """
    operations = {"+":my_add, "-":my_sub, "*":my_mul, "/":my_truediv, "//":my_floordiv, "%":my_mod, "**":my_pow}
    f_op = try_convert_number(get_user_input("Enter first number").strip())
    s_op = try_convert_number(get_user_input("Enter second number").strip())
    op = get_user_input("Enter operation one of (+,-,*,/,//,%,**)").strip()
    if op not in operations.keys():
        raise ValueError(f"Operation {op} is not supported")

    result = operations[op](f_op, s_op)
    print(f"execute: {f_op} {op} {s_op} = {result}")

    return result

if __name__ == "__main__":
    my_debug = False
    if my_debug:
        print("Simple tests:")
        print("="*10)
       
        print("try_convert_number(value):")
        assert try_convert_number(2) == 2, "Error: 2 are number float"
        assert try_convert_number("2") == 2, "Error: '2' are number float"
        assert try_convert_number(2.45) == 2.45, "Error: 2.45 are number float"
        assert try_convert_number("2.45") == 2.45, "Error: '2.45' are number float"
        assert try_convert_number("23.2.45") is None, "Error: '23.2.45' are not number float"
        assert try_convert_number("boo") is None, "Error: 'boo' are not number float"
        assert try_convert_number("boo.baz") is None, "Error: 'boo.baz' are not number float"
        assert try_convert_number(["boo", "baz"]) is None, "Error: ['boo', 'baz'] are not number float"
        assert try_convert_number([22]) is None, "Error: [22] are not number float"
        assert try_convert_number((22,)) is None, "Error: (22,) are not number float"
        assert try_convert_number({22}) is None, "Error: {22} are not number float"
        assert try_convert_number({"value":22}) is None, "Error: {'value': 22} are not number float"
        assert try_convert_number(None) is None, "Error: None are not number float"
        print("-"*78)

        print("test_operands(l_operand, r_operand):")
        assert test_operands(2, 2), "Error: 2, 2 are numbers"
        assert test_operands(1.2, 1.7), "Error: 1.2, 1.7 are numbers"
        assert not test_operands("3", 7), "Error: value '3' is not supported"
        assert not test_operands(3, {7}), "Error: value \{7\} not supported"
        assert not test_operands([3,], (7,)), "Error: values [3] and (7,) not supported"
        assert not test_operands([], ()), "Error: values [] and (,) not supported"
        print("-"*78)

        print("my_add(l_operand, r_operand):")
        assert my_add(2, 2) == 4, "Error: 2+2 != 4"
        assert my_add(1.2, 1.7) == 2.9, "Error: 1.2+1.7 != 2.9"
        assert my_add(0.0, 1.7) == 1.7, "Error: 0.0+1.7 != 1.7"
        assert my_add(1.2, 0) == 1.2, "Error: 1.2+0 != 1.2"
        print("-"*78)

        print("my_sub(l_operand, r_operand):")
        assert my_sub(2, 2) == 0, "Error: 2-2 != 0"
        assert my_sub(2.1, 2.1) == 0.0, "Error: 2.1-2.1 != 0.0"
        assert my_sub(1.2, 1.7) == -0.5, "Error: 1.2-1.7 != -0.5"
        assert my_add(0.0, 1.7) == 1.7, "Error: 0.0-1.7 != -1.7"
        assert my_add(1.2, 0) == 1.2, "Error: 1.2-0 != 1.2"
        print("-"*78)

        print("my_mul(l_operand, r_operand):")
        assert my_mul(2, 2) == 4, "Error: 2*2 != 4"
        assert my_mul(2.1, 2.1) == 4.41, "Error: 2.1*2.1 != 4.41"
        assert my_mul(1.2, 1.7) == 2.04, "Error: 1.2*1.7 != 2.04"
        assert my_mul(0.0, 1.7) == 0, "Error: 0.0*1.7 != 0"
        assert my_mul(1.2, 0) == 0, "Error: 1.2*0 != 0"
        print("-"*78)

        print("my_truediv(l_operand, r_operand):")
        assert my_truediv(2, 2) == 1, "Error: 2/2 != 1"
        assert my_truediv(2.1, 2.1) == 1, "Error: 2.1/2.1 != 1"
        assert round(my_truediv(1.2, 1.7), 2) == 0.71, "Error: round(1.2/1.7,2) != 0.71"
        assert my_truediv(0.0, 1.7) == 0, "Error: 0.0/1.7 != 0"
        try:
            my_truediv(1.2, 0)
        except ZeroDivisionError as ex:
            pass
        else:
            print("Error: 1.2 / 0 != Exception")
        print("-"*78)

        print("my_floordiv(l_operand, r_operand):")
        assert my_floordiv(3, 2) == 1, "Error: 3//2 != 1"
        assert my_floordiv(12.1, 2.1) == 5.0, "Error: 12.1//2.1 != 5.0"
        assert my_floordiv(12, 7) == 1, "Error: 12//7,2 != 1"
        assert my_floordiv(0, 7) == 0, "Error: 0//7 != 0"
        try:
            my_truediv(24, 0)
        except ZeroDivisionError as ex:
            pass
        else:
            print("Error: 24 // 0 != Exception")
        print("-"*78)

        print("my_mod(l_operand, r_operand):")
        assert my_mod(3, 2) == 1, "Error: 3%2 != 1"
        assert round(my_mod(12.1, 2.1), 2) == 1.6, "Error: round(12.1%2.1, 2) != 1.6"
        assert my_mod(12, 7) == 5, "Error: 12%7 != 5"
        assert my_mod(0, 7) == 0, "Error: 0%7 != 0"
        try:
            my_mod(24, 0)
        except ZeroDivisionError as ex:
            pass
        else:
            print("Error: 24 % 0 != Exception")
        print("-"*78)

        print("my_pow(l_operand, r_operand):")
        assert my_pow(3, 2) == 9, "Error: 3**2 != 9"
        assert round(my_pow(12.1, 2.1), 2) == 187.87, "Error: round(12.1 ** 2.1, 2) != 187.87"
        assert my_pow(12, 7) == 35831808, "Error: 12 ** 7 != 35831808"
        assert my_pow(0, 7) == 0, "Error: 0 ** 7 != 0"
        assert my_pow(24, 0) == 1, "Error: 24 ** 0 != 1"
        print("-"*78)

    print("General call function boo:")
    print(boo())