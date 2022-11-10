# select_stack_bills.py
# 
# Модуль, що займається формуванням набору доступних банкнот 
# у нашому віртуальному банкоматі
# 

from collections.abc import Iterable
from itertools import zip_longest


AVIALIBLE_NOMINALS_BILLS = (10, 20, 50, 100, 200, 500, 1000)


class NotEnoughCostInATMError(Exception):
    """ Виключна ситуація - не достатньо коштів у банкоматі """


class NotPossibleSelectSetBanknotesError(Exception):
    """ Виключна ситуація - не вдалося підібрати потрібні купюри """


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
    tmpzip = map(
        lambda item2: (item2[0], 0) if item2[1] is None else item2, 
        filter(
           lambda item: item[0], zip_longest(AVIALIBLE_NOMINALS_BILLS, seq)
           )
        )
    try:
        dct = {nominal: int(cnt) for nominal, cnt in tmpzip}
    except TypeError:
        print(f"Error. create_stack_bills: Positional parameters must be only \
int numbers. You pass: {seq}")
        raise
    return dct


def seq_intandint_to_dict_stack_bills(seq):
    """
    Перетворення послідовності виду ((key::int, value::int) у
    словник => {key: value, ... }

    input:
        Структура даних, що повертається від SELECT запиту з sqlite
    return:
        Словник - Заповнена "касета з банкнотами"
        Або виключення TypeError
    """
    tmp = map(lambda item: (
        remove_non_digit_char(str(item[0])),
        remove_non_digit_char(str(item[1]))
        ), seq) 
    try:
        dct = {int(nominal): int(cnt) for nominal, cnt in tmp}
    except TypeError:
        print(f"Error. seq_intandint_to_dict_stack_bills: Parameters must be \
only int numbers or to be transform to int. You pass: {seq}")
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
    # обробка параметрів
    params = None
    if len(args) > 0:
        if isinstance(args[0], Iterable):
            if len(args) > 1 and all(
                    map(lambda arg: isinstance(arg, Iterable), args)):
                params = seq_intandint_to_dict_stack_bills(args)
            else:
                if isinstance(args[0], dict):
                    params = args[0]
                elif all(map(
                    lambda item: isinstance(item, Iterable) and len(item) == 2,
                    args[0])
                ):
                    params = seq_intandint_to_dict_stack_bills(args[0])
                else:
                    params = seqint_to_dict_stack_bills(args[0])
        else:
            params = seqint_to_dict_stack_bills(args)
    elif len(kwargs) > 0:
        params = {
            remove_non_digit_char(key): value for key, value in kwargs.items()}
    else:
        params = {}

    # Формування результату
    stack = {}
    for key in AVIALIBLE_NOMINALS_BILLS:
        stack[key] = params.get(key, 0)

    return stack


def get_stack_balance(stack):
    """
    Обчислення максимально можливої суми наявної у касеті
    банкомата 

    return:
        Баланс ATM
    """
    return sum(nominal * cnt for nominal, cnt in stack.items())


def is_present_enough_cost_atm(value, stack_atm):
    """
    Перевірка чи достатньо коштів у касеті банкомата

    Input:
        value        - сума яку порібно перевірити
        stack_atm    - словник наявних купюр в ATM

    Return:
        bool - Достатньо чи ні наявних банкнот

    """
    return value <= get_stack_balance(stack_atm)


def form_appropriate_stack(
        value_in, stack_atm, nominal, stack_user_work, 
        value_need, level):
    """
    Функція, що реалізує алгоритм підбору купюр до видачі
    За основу взятий 

    Input:
        value        - сума яку порібно видати
        stack_atm    - словник наявних купюр в ATM
        stack_user_work - банкноти, що вже підібрані, для початку заносимо сюди
         першу кільність банкнот яка можлива відновідного номіналу, обрахунок 
         починаємо із банкноти попереднього номінала

    Return:
        cловник підібраних купюр
        Виключна ситуація ValueError - якщо підбір завершився невдачею
    """
    need_bills = value_in // nominal
    if need_bills > stack_atm[nominal]:
        # якщо наявно менше банкнот ніж потребується зменшуємо до наявних
        need_bills = stack_atm[nominal]

    if value_in == 0:
        return stack_user_work
    if nominal == AVIALIBLE_NOMINALS_BILLS[0]:
        if need_bills <= stack_atm[nominal]:
            stack_user_work[nominal] = need_bills
            return stack_user_work
    else:
        if need_bills == 0:
            stack_result = form_appropriate_stack(
                value_in, stack_atm, prev_nominal(nominal), stack_user_work, 
                value_need, level+1)
            return stack_result
        else:
            for cur_cnt_bills in range(need_bills, -1, -1):
                try:
                    stack_user_work[nominal] = cur_cnt_bills
                    stack_result = form_appropriate_stack(
                        value_in - nominal * cur_cnt_bills, stack_atm, 
                        prev_nominal(nominal), stack_user_work, value_need, 
                        level+1)
                    if get_stack_balance(stack_user_work) == value_need:
                        return stack_user_work
                    continue
                except NotPossibleSelectSetBanknotesError:
                    pass

    if value_need == get_stack_balance(stack_user_work):
        return stack_user_work
    raise NotPossibleSelectSetBanknotesError(
        f"Error: form_appropriate_stack({value_in}, av.stack:{stack_atm}) in \
process my select{stack_user_work}")


def prev_nominal(nominal):
    """
    Знаходими попередній номінал із доступних
    """
    if nominal not in AVIALIBLE_NOMINALS_BILLS:
        raise KeyError(f"prev_nominal: {nominal} not present")

    idx = AVIALIBLE_NOMINALS_BILLS.index(nominal)

    if idx - 1 < 0:
        raise KeyError("prev_nominal: for 10 is not present")
    return AVIALIBLE_NOMINALS_BILLS[idx - 1]


def form_stack_bills(value, stack_atm):
    """
    Функція, пробує підібрати суму купюрами, враховуючи їх наявність
    різнимим способами
        - Жадний алгоритм
        - Рекурсивний підбір із модифікацією поточних умов
        - Повний перебір варіантів(варіант останної надії), якщо попередні 
        не справились

    Input:
        value       - сума яку порібно видати
        stack_atm   - словник наявних купюр в банкоматі

    Return:
        cловник підібраних купюр
        Exception:
            NotEnoughCostInATMError     - не достатньо коштів у банкоматі
            NotPossibleSelectSetBanknotesError - не вдалося підібрати потрібні
              банкноти
    """
    if get_stack_balance(stack_atm) > value:
        nominal = None
        stack_user_current = create_stack_bills()
        for cur_nominal in sorted(AVIALIBLE_NOMINALS_BILLS, reverse=True):
            if value // cur_nominal > 0:
                nominal = cur_nominal
                cnt_nominal = value // nominal
                break

        for cur_cnt_nominal in range(cnt_nominal, 0, -1):
            try:
                stack_result = form_appropriate_stack(
                    value, stack_atm, nominal, stack_user_current, value, 0)
            except NotPossibleSelectSetBanknotesError:
                pass
            else:
                return stack_result
        raise NotPossibleSelectSetBanknotesError(f"Sorry we do not find need \
combination for :{value} atm_stack:{stack_atm}")
    else:
        raise NotEnoughCostInATMError(f"Attention. ATM does not contain \
enough cost. Try value {get_stack_balance(stack_atm)} or less")
