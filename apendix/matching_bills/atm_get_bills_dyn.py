# atm_get_bills_dyn.py
from collections.abc import Iterable
from itertools import zip_longest


AVIALIBLE_NOMINALS_BILLS = (10, 20, 50, 100, 200, 500, 1000)


def form_apropriate_stack_dyn(value, stack_atm):
    """Підбір купюр наявних у банкоматі (stack_atm) для формування необхідної
     суми value

    Input:
        value - сума яку треба видати
        stack_atm - набір купюр банкомата у форматі словника:
            номінал: кількість 
            {10: 0, 20: 2, 50: 1, 100: 0, 200: 1, 500: 1, 1000: 0} 
    Return:
        набір купюр до видачі у форматі словника
     """
    def combine_tpl_val(tpl, value):
        """Допоміжна внутрішня ф-ія що,
        формує кортеж із існуючого та нового значення"""
        lst = list(tpl)
        lst.append(value)
        return tuple(lst)

    def list_stack_to_dict(lst):
        """Допоміжна внутрішня ф-ія що,
        проводить перетворення списка потрібних банкнот в словник: 
            {номінал: кількість, }"""
        dct = {}
        for item in lst[1:]:
            dct[item] = dct.get(item, 0) + 1
        return dct

    print(f"{stack_atm=}")
    lst_atm = [
        nominal for nominal, cnt in stack_atm.items() for _ in range(cnt)
        ]
    lst_atm.reverse()

    lst_prev_keep = [(0, (0,))]
    for i in range(len(lst_atm)):
        lst_keep = []
        nominal_cur = lst_atm[i]
        for prev_value, prev_tpl in lst_prev_keep:
            lst_keep.append(
                (prev_value + nominal_cur, 
                 combine_tpl_val(prev_tpl, nominal_cur))
                )

        if any(map(lambda item: value == item[0], lst_keep)):
            for keep_sum, stack in lst_keep:
                if keep_sum == value:
                    return list_stack_to_dict(stack)

        lst_prev_keep.extend(lst_keep)

        lst_prev_keep = list(
            filter(lambda item: item[0] < value, lst_prev_keep))

    raise ValueError(
        f"Attention sum:{value} do not combine in stack: {stack_atm}")


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


def process_test(value, test_stack_atm):
    """Функція тільки для тестування"""
    print(f"{test_stack_atm=}")
    try:
        stack_result = form_apropriate_stack_dyn(value, test_stack_atm)
        print(f"sum:{value} {stack_result=} "
              f"{sum(nominal * cnt for nominal, cnt in stack_result.items())}")
    except ValueError as ex:
        print(f"Не вдалося підібрати. {value}", ex)
    print()


if __name__ == "__main__":
    process_test(1880, create_stack_bills((1, 1, 1, 1, 1, 1, 1)))

    process_test(1350, create_stack_bills((2, 2, 2, 2, 2, 2, 2)))

    process_test(110, create_stack_bills((2, 2, 2, 2, 2, 2, 2)))

    # 2.1 Сума 110 що видається при відсутності 10
    process_test(110, create_stack_bills((0, 5, 2, 2, 2, 2, 2)))
    
    process_test(1780, create_stack_bills(
        {10: 3, 20: 0, 50: 3, 100: 1, 200: 0, 500: 1, 1000: 1}))

    process_test(110, create_stack_bills(
        {10: 0, 20: 3, 50: 1, 100: 0, 200: 0, 500: 0, 1000: 0}))

# від Valerii Danilov
    process_test(1170, create_stack_bills(
        {10: 5, 20: 1, 50: 1, 100: 0, 200: 4, 500: 1, 1000: 5}))

    process_test(1100, create_stack_bills(
        {10: 5, 20: 1, 50: 1, 100: 0, 200: 4, 500: 1, 1000: 5}))

    process_test(1200, create_stack_bills(
        {10: 5, 20: 1, 50: 1, 100: 0, 200: 4, 500: 1, 1000: 5}))

    # жлважвіл
    # 20 -> 0, 10 -> 2
    process_test(20, create_stack_bills(
        {10: 2, 20: 0, 50: 0, 100: 0, 200: 0, 500: 0, 1000: 0}))

# Збійні варіанти
    process_test(760, create_stack_bills(
        {10: 0, 20: 2, 50: 1, 100: 0, 200: 1, 500: 1, 1000: 0}))


