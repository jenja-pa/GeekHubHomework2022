# yelding_bill.py

# Модуль, з функцією, що займається видачею суми купюрами
from collections.abc import Iterable
from itertools import zip_longest


AVIALIBLE_NOMINALS_BILLS = (10, 20, 50, 100, 200, 500, 1000)


# def create_empty_stack_bills():
#     """
#     Допоміжна функція створення пустого словника для фіксації 
#     якогось поточного набору купюр
#     """
#     return {nominal: 0 for nominal in AVIALIBLE_NOMINALS_BILLS}


def seqint_to_dict_stack_bills(seq):
    """
    Перетворення послідовності int значень у dict із ключами 
    AVIALIBLE_NOMINALS_BILLS

    Input:
        seq     - послідовність цілих чисел

    Output:
        Словник - Заповнена "касета з банкнотами"
        Або виключення TypeError
    """
    try:
        tmpzip = map(
            lambda item2: (item2[0], 0) if item2[1] is None else item2, 
            filter(
               lambda item: item[0], zip_longest(AVIALIBLE_NOMINALS_BILLS, seq)
               )
            )
        dct = {nominal: int(cnt) for nominal, cnt in tmpzip}
    except TypeError:
        print(f"Error. create_stack_bills: Positional parameters must be only \
int numbers you pass: {seq}")
        raise
    return dct


def remove_non_digit_char(value):
    """
    Функція вилучає із value не числові символи та перетворює перше число, що 
    зустрінеться на int

    Input:
        string рядок
    Return:
        Визначене число типу int або 0
    """
    tmp = "".join(
        map(lambda item: item if item.isdigit() else " ", str(value))
        ).split()

    return int(tmp[0]) if len(tmp) > 0 else 0


def create_stack_bills(*args, **kwargs):
    """
    Допоміжна функція створення деякого набору стану касети з купюрами
    """
    print(f"{args=}, {kwargs=}")
    # обробка параметрів
    params = None
    if len(args) > 0:
        # Передані позиційні параметри
        if isinstance(args[0], Iterable):
            # Першим параметром передано послідовність - використовуємо тільки
            # його, навіть якщо існують інші позиційні
            if isinstance(args[0], dict):
                # якщо перший параметр словник просто беремо його для роботи
                params = args[0]
            else:
                # перший параметр не словник, перетворюємо його у словник
                # ключі AVIALIBLE_NOMINALS_BILLS
                params = seqint_to_dict_stack_bills(args[0])
        else:
            # Перший параметр не послідовність - вважаємо, що отримано перелік
            # позиційних аргументів типу int
            params = seqint_to_dict_stack_bills(args)
    else:
        # Передано іменовані параметри із даними
        print("Pass kwargs arguments")
        # Осільки іменовані параметри не можуть бути числом, - потрібно їх
        # визначити із ключів kwargs видаливши не цифри
        params = {
            remove_non_digit_char(key): value for key, value in kwargs.items()}
    # Формування результату
    # створення структури пустої касети для купюр, яку заповнимо даними
    # переданих параметрів
    # stack = {nominal: 0 for nominal in AVIALIBLE_NOMINALS_BILLS}
    stack = {}
    for key in AVIALIBLE_NOMINALS_BILLS:
        stack[key] = params.get(key, 0)

    return stack


def yielding_bills(value, nominal, stack_present, stack_output):
    """
    Функція, що рекурсивно займається підбором суми купюрами, враховуючи
    їх наявність

    Input:
        value            - сума яку порібно видати
        nominal          - поточний номінал купючи з якої починаємо пошук
        stack_present    - словник наявних купюр
        stack_output     - словник`` підібраних купюр

    Return:
        cловник підібраних купюр
    """


if __name__ == "__main__":
    # Тестування роботи

    print("1. перевірка remove_non_digit_char()")
    cases = [
        {
            "message": "1. Правильне число",
            "func": remove_non_digit_char, "params": (123, ),
            "true_result": 123
        }, {
            "message": "2. Правильне число рядок",
            "func": remove_non_digit_char, "params": ("123", ),
            "true_result": 123
        }, {
            "message": "3. Рядок з літерою спочатку",
            "func": remove_non_digit_char, "params": ("b123", ),
            "true_result": 123
        }, {
            "message": "3.1 Рядок з літерами спочатку",
            "func": remove_non_digit_char, "params": ("boob123", ),
            "true_result": 123
        }, {
            "message": "4. Рядок з літерою в кінці",
            "func": remove_non_digit_char, "params": ("123а", ),
            "true_result": 123
        }, {
            "message": "4.1 Рядок з літерами в кінці",
            "func": remove_non_digit_char, "params": ("123арррра", ),
            "true_result": 123
        }, {
            "message": "5. Рядок з літерою спочатку і в кінці",
            "func": remove_non_digit_char, "params": ("e123а", ),
            "true_result": 123
        }, {
            "message": "5.1 Рядок з літерами спочптку і в кінці",
            "func": remove_non_digit_char, "params": ("lskjf123арррра", ),
            "true_result": 123
        }, {
            "message": "6 Рядок з літерами та декілька груп чисел",
            "func": remove_non_digit_char, "params": ("lf123арр458рр789а", ),
            "true_result": 123
        }, {
            "message": "7 Рядок тільки з літерами",
            "func": remove_non_digit_char, "params": ("lskjfарррра", ),
            "true_result": 0
        }, {
            "message": "7 Пустий рядок",
            "func": remove_non_digit_char, "params": ("", ),
            "true_result": 0
        }
        ]
    for case in cases:
        print(f"{case['message']}: {case['func'].__name__}{case['params']} => \
{case['func'](*case['params'])} == {case['true_result']}")

    print("-"*45)

    print("2. Перевірка create_stack_bills з різними видами параметрів")
    print("1 варіант передачі позиційних параметрів")
    result = create_stack_bills(2, 3, 4, 5, 6)

    print("2 варіант передачі 1й позиційний параметр dict")
    result = create_stack_bills(
        {10: 3, 20: 0, 50: 23, 100: 18, 75: 4}, 2, 3, 4, 5, 6)

    print("3 варіант передачі 1й позиційний параметр seq - tuple")
    result = create_stack_bills((3, 0, 23, 18, 75), 2, 3, 4, 5, 6)

    print("4 варіант передачі 1й позиційний параметр seq - list")
    result = create_stack_bills([3, 0, 23, 18, 75], 2, 3, 4, 5, 6)

    print("5 варіант передачі іменовані аргументи")
    result = create_stack_bills(p10=2, p50=3, b200=4, f500=5, k1000=6)
    print("-"*45)

    print("3. Перевірка yielding_bill")
    print("1 варіант передачі позиційних параметрів")

    # yielding_bill(value, nominal, stack_present, stack_output):
