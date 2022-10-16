# task_2.py
# Створіть 3 рiзних функцiї (на ваш вибiр). 
# Кожна з цих функцiй повинна повертати якийсь результат (напр. інпут 
#  від юзера, результат математичної операції тощо). 
# Також створiть четверту ф-цiю, яка всередині викликає 3 попередні, 
#  обробляє їх результат та також повертає результат своєї роботи. 
# Таким чином ми будемо викликати одну (четверту) функцiю, а вона в 
#  своєму тiлi - ще 3.
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


def process(a, b):
    """
    Функція що проводить різні операцію обчислення
    """
    print(f"{a} + {b} = {a + b}")
    print(f"{a} - {b} = {a - b}")
    print(f"{a} * {b} = {a * b}")
    print(f"{a} / {b} = {a / b}")
    print(f"{a} // {b} = {a // b}")
    print(f"{a} % {b} = {a % b}")
    print(f"{a} ** {b} = {a ** b}")
    print(f"{a} << {b} = {a << b}")

    return None



def boo():
    """
    Функція, що проводить визов інщих функцій
    """
    a = try_convert_number(get_user_input("Enter number A").strip())
    b = try_convert_number(get_user_input("Enter number B").strip())

    process(a, b)

    return None

if __name__ == "__main__":
    boo()