# yelding_bill.py
# !!!!!!!!!!!!!!!!!!!!!!!!!!!
# Це робочий фпйл, з кучею лишньої інформації для відладки(самопальні тести), 
# прошу не звертати на нього увагу
# 
# Я хочу зберегти цей файл, щоб можливо проводити відладку якщо будуть 
# зауваження до його роботи, я це на даний момент роблю без відладчика, тому щоб
# не розставляти заново всі пояснення та відладочні прінти залишу його тут, 
# звичайно його треба якось сховати, але я ще не знаю як.
# 
# Правильний модуль розміщено у файлі:
#   select_stack_bills.py
# !!!!!!!!!!!!!!!!!!!!!!!!!!

# Модуль, з функцією, що займається видачею суми купюрами
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
        # Передані позиційні параметри
        if isinstance(args[0], Iterable):
            # Першим параметром передано послідовність
            if len(args) > 1 and all(
                    map(lambda arg: isinstance(arg, Iterable), args)):
                # Якщо всі позиційні аргументи послідовності, то вважаємо, що 
                # вони представляють собою набір виду 
                # ((key::int, value::int), ...)
                params = seq_intandint_to_dict_stack_bills(args)
            else:
                # Якщо тільки перший аргумент послідовність - використовуємо 
                # тільки його, навіть якщо існують інші позиційні
                if isinstance(args[0], dict):
                    # якщо перший параметр словник просто беремо його
                    params = args[0]
                elif all(map(
                    lambda item: isinstance(item, Iterable) and len(item) == 2,
                    args[0])
                ):
                    # Варіант передачі кортежем чи списком виду 
                    # ((key, val), ... )
                    params = seq_intandint_to_dict_stack_bills(args[0])
                else:
                    # перший параметр не словник, перетворюємо його у словник
                    # ключі AVIALIBLE_NOMINALS_BILLS
                    params = seqint_to_dict_stack_bills(args[0])
        else:
            # Перший параметр не послідовність - вважаємо, що отримано перелік
            # позиційних аргументів типу int
            params = seqint_to_dict_stack_bills(args)
    elif len(kwargs) > 0:
        # Передано іменовані параметри із даними
        # print("Pass kwargs arguments")
        # Осільки іменовані параметри не можуть бути числом, - потрібно їх
        # визначити із ключів kwargs видаливши не цифри
        params = {
            remove_non_digit_char(key): value for key, value in kwargs.items()}
    else:
        # Не передано жодного параметра - формуємо пустий словник(касету)
        params = {}
    # Формування результату
    # створення структури пустої касети для купюр, яку заповнимо даними
    # переданих параметрів
    # stack = {nominal: 0 for nominal in AVIALIBLE_NOMINALS_BILLS}
    stack = {}
    for key in AVIALIBLE_NOMINALS_BILLS:
        stack[key] = params.get(key, 0)

    return stack


def get_stack_balance(stack):
    """
    Обчислення максимально можливої суми наявною у банкоматі

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


def greedy_select(value_in, stack_atm, nominal, stack_user_work, value_need, level):
    """
    Жадний алгоритм підбору купюр до видачі

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
    # print(f"greedy_select: {value_in=}, {value_need=}, {stack_atm=}, {nominal=}, {stack_user_work=}, {level=}")

    need_bills = value_in // nominal
    if need_bills > stack_atm[nominal]:
        # якщо наявно менше банкнот ніж потребується зменшуємо до наявних
        need_bills = stack_atm[nominal]

    # print(f"{need_bills=}, {nominal=}")

    if value_in == 0:
        # сума підібрана повертаємо результат
        # print("-----------")
        # print(f"сума підібрана повертаємо результат: {stack_user_work=}, balans:{get_stack_balance(stack_user_work)} {level=}")
        # print("-----------")
        return stack_user_work
    if nominal == AVIALIBLE_NOMINALS_BILLS[0]:
        # end of recursion
        if need_bills <= stack_atm[nominal]:
            # банкнот достатньо
            stack_user_work[nominal] = need_bills
            return stack_user_work
        # else:
        #     NotPossibleSelectSetBanknotesError("Не достатньо банкнот")
    else:
        # deep recursion
        # print(f"deep recursion {level=}")
        if need_bills == 0:
            # пропуск номінала
            stack_result = greedy_select(value_in, stack_atm, prev_nominal(nominal), stack_user_work, value_need, level+1)
            return stack_result
        else:
            # пробуємо використати номінал
            # print("else rec")
            for cur_cnt_bills in range(need_bills, -1, -1):
                try:
                    # print(f"for {cur_cnt_bills}")
                    stack_user_work[nominal] = cur_cnt_bills
                    stack_result = greedy_select(value_in - nominal * cur_cnt_bills, stack_atm, prev_nominal(nominal), stack_user_work, value_need, level+1)
                    # print("test")
                    if get_stack_balance(stack_user_work) == value_need:
                        # print(f"Вдалося підібрати банкноти: Сума({value_in}) {stack_user_work} : перевірка({get_stack_balance(stack_user_work)}) {level=}")
                        return stack_user_work
                    continue
                except NotPossibleSelectSetBanknotesError as ex:
                    # print(f"greedy_select: - NotPossibleSelectSetBanknotesError======={level}")
                    # print(f"{ex} {level}")
                    # print(f"Спроба з {cur_cnt_bills} bill:{nominal} Не вдалося підібрати банкноти для Суми({value_in}) ATM state:{stack_atm}, Зробимо коригування та пробуємо ще раз")        
                    pass




        # result = create_stack_bills()
        # value = value_in
        # # print(value)
        # for nominal in sorted(AVIALIBLE_NOMINALS_BILLS, reverse=True):
        #     cnt_to_get = 0
        #     if value // nominal > stack_atm[nominal]:
        #         cnt_to_get = stack_atm[nominal]
        #     else:
        #         cnt_to_get = value // nominal

        #     result[nominal] = cnt_to_get
        #     value = value - nominal * cnt_to_get
            # print(f"{nominal} * {cnt_to_get}, {value}")

        # print(f"rest:{value}")
    # if value == 0.0:
    #     return result
    # print(f"before raise NotPossibleSelectSetBanknotesError select-stack:{get_stack_balance(stack_user_work)} - {value_need=}")
    if value_need == get_stack_balance(stack_user_work):
        return stack_user_work
    raise NotPossibleSelectSetBanknotesError(f"Error: greedy_select({value_in}, \
av.stack:{stack_atm}) in process my select{stack_user_work}")

    # Функція, що рекурсивно займається підбором суми купюрами, враховуючи
    # їх наявність
    # nominal          - поточний номінал купючи з якої починаємо пошук


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


def yielding_bills(value, stack_atm):
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
        # case 1 - Пробуємо підібрати набір жадним алгоритмом
        nominal = None
        stack_user_current = create_stack_bills()
        for cur_nominal in sorted(AVIALIBLE_NOMINALS_BILLS, reverse=True):
            if value // cur_nominal > 0:
                nominal = cur_nominal
                cnt_nominal = value // nominal
                break

        # початок підбору
        # print(f"yielding_bills: {value=}, {stack_atm=}, {nominal=}, {cnt_nominal=}")
        # print(f"{nominal=} , {cnt_nominal=}")
        # print(tuple(range(cnt_nominal, 0, -1)))
        for cur_cnt_nominal in range(cnt_nominal, 0, -1):
            try:
                stack_result = greedy_select(value, stack_atm, nominal, stack_user_current, value, 0)
                # print("test2")
            except NotPossibleSelectSetBanknotesError:
                pass
                # print(f"Спроба з {cur_cnt_nominal} bill:{nominal} Не вдалося підібрати банкноти для Суми({value}) ATM state:{stack_atm}")        
            else:
                # print(f"Вдалося підібрати банкноти: Сума({value}) {stack_result} : перевірка({get_stack_balance(stack_result)})")
                return stack_result
        # print(f"Не вдалося підібрати банкноти для Суми({value}) ATM state:{stack_atm}")
        raise NotPossibleSelectSetBanknotesError(f"Sorry we do not find need combination for :{value} atm_stack:{stack_atm}")
    else:
        raise NotEnoughCostInATMError(f"Attention. ATM does not contain enough cost. Try value {get_stack_balance(stack_atm)} or less")


if __name__ == "__main__":
    # test 110 без 10
    value = 110
    print(f"yielding_bills({value}, atm:{create_stack_bills(p20=5, p50=4, p100=2)})")
    result = yielding_bills(value, create_stack_bills(create_stack_bills(p20=5, p50=4, p100=2)))
    print(value, tuple(map(lambda el: (el[1], el[0]), filter(lambda item: item[1], result.items()))))
    
    # Valerii Danilov  1170 1100 до 1200)
    value = 1170
    print(f"yielding_bills({value}, atm:{create_stack_bills([(1000, 5), (500, 1), (200, 4), (100, 0), (50, 1), (20, 1), (10, 5)])})")
    result = yielding_bills(value, create_stack_bills([(1000, 5), (500, 1), (200, 4), (100, 0), (50, 1), (20, 1), (10, 5)]))
    print(value, tuple(map(lambda el: (el[1], el[0]), filter(lambda item: item[1], result.items()))))
    
    value = 1100
    print(f"yielding_bills({value}, atm:{create_stack_bills([(1000, 5), (500, 1), (200, 4), (100, 0), (50, 1), (20, 1), (10, 5)])})")
    result = yielding_bills(value, create_stack_bills([(1000, 5), (500, 1), (200, 4), (100, 0), (50, 1), (20, 1), (10, 5)]))
    print(value, tuple(map(lambda el: (el[1], el[0]), filter(lambda item: item[1], result.items()))))
    
    value = 1200
    print(f"yielding_bills({value}, atm:{create_stack_bills([(1000, 5), (500, 1), (200, 4), (100, 0), (50, 1), (20, 1), (10, 5)])})")
    result = yielding_bills(1200, create_stack_bills([(1000, 5), (500, 1), (200, 4), (100, 0), (50, 1), (20, 1), (10, 5)]))
    print(value, tuple(map(lambda el: (el[1], el[0]), filter(lambda item: item[1], result.items()))))

    # my find variants
    value = 3990
    stack_atm = [3, 3, 0, 4, 5, 1, 5]
    print(f"yielding_bills({value}, atm:{create_stack_bills(stack_atm)})")
    result = yielding_bills(value, create_stack_bills(stack_atm))
    print(value, tuple(map(lambda el: (el[1], el[0]), filter(lambda item: item[1], result.items()))))

    value = 4300
    stack_atm = [5, 1, 2, 0, 1, 2, 4] 
    print(f"yielding_bills({value}, atm:{create_stack_bills(stack_atm)})")
    result = yielding_bills(value, create_stack_bills(stack_atm))
    print(value, tuple(map(lambda el: (el[1], el[0]), filter(lambda item: item[1], result.items()))))

    value = 4300
    stack_atm = [5, 1, 2, 2, 0, 2, 4] 
    print(f"yielding_bills({value}, atm:{create_stack_bills(stack_atm)})")
    result = yielding_bills(value, create_stack_bills(stack_atm))
    print(value, tuple(map(lambda el: (el[1], el[0]), filter(lambda item: item[1], result.items()))))

    print()
    print()
    print("Random test:")
    print("-"*10)
    import random
    for idx in range(20):
        value = random.randint(300, 700) * 10
        stack_atm = [random.randint(0,5) for _ in range(7)]
        print(f"{value=}, {stack_atm=}")
        print(f"yielding_bills({value}, atm:{create_stack_bills(stack_atm)})")
        try:
            result = yielding_bills(value, create_stack_bills(stack_atm))
            print(value, tuple(map(lambda el: (el[1], el[0]), filter(lambda item: item[1], result.items()))))
            print("+"*10)
        except NotEnoughCostInATMError:
            pass
        except NotPossibleSelectSetBanknotesError as ex:
            print(f"Not variants {ex}")
            print("+"*10)



#     # Тестування роботи - Самопальне

#     # yielding_bill(value, nominal, stack_present, stack_output):
#     print("V. перевірка greedy_select(value, stack_present) - \
# Жадний алгоритм підбору")
#     cases = [
#         {
#             "message": "1. Сума що правильно видається",
#             "func": greedy_select, "params": (1880, create_stack_bills(
#                 (1, 1, 1, 1, 1, 1, 1))),
#             "true_result": 
#                 {10: 1, 20: 1, 50: 1, 100: 1, 200: 1, 500: 1, 1000: 1},
#             "expexted_exception": False
#         }, {
#             "message": "2. Сума що правильно видається",
#             "func": greedy_select, "params": (1350, create_stack_bills(
#                 (2, 2, 2, 2, 2, 2, 2))),
#             "true_result": 
#                 {10: 0, 20: 0, 50: 1, 100: 1, 200: 1, 500: 0, 1000: 1},
#                 "expexted_exception": False
#         }, {
#             "message": "2. Сума 110 що правильно видається при наявності 10",
#             "func": greedy_select, "params": (110, create_stack_bills(
#                 (2, 2, 2, 2, 2, 2, 2))),
#             "true_result": 
#                 {10: 1, 20: 0, 50: 0, 100: 1, 200: 0, 500: 0, 1000: 0},
#             "expexted_exception": False
#         }, {
#             "message": 
#                 "2.1 Сума 110 що неправильно видається при відсутності 10",
#             "func": greedy_select, "params": (110, create_stack_bills(
#                 (0, 5, 2, 2, 2, 2, 2))),
#             "true_result": 
#                 {10: 0, 20: 3, 50: 1, 100: 0, 200: 0, 500: 0, 1000: 0},
#             "expexted_exception": True
#         }]
#     for case in cases:
#         if not case["expexted_exception"]:
#             if not case['func'](*case['params']) == case['true_result']:
#                 print(f"{case['message']}: \
# {case['func'].__name__}{case['params']} => {case['func'](*case['params'])} == \
# {case['true_result']} : ('Error')")
#                 print("-"*15)
#         else:
#             try:
#                 case['func'](*case['params']) 
#             except ValueError:
#                 # Right exception 
#                 pass
#             else:
#                 # Exception do not raise - It is no good
#                 print(f"{case['message']}: \
# {case['func'].__name__}{case['params']} => {case['func'](*case['params'])} == \
# {case['true_result']} : ('Need Exception but Nothing')")
#                 print("-"*15)
#     print("-"*45)


#     print("III. перевірка get_sum_cost_atm(stack_atm)")
#     cases = [
#         {
#             "message": "1. набір:  {10: 3, 20: 0, 50: 3, 100: 1, 200: 0, 500: 1, 1000: 1}",
#             "func": get_sum_cost_atm, "params": (create_stack_bills({10: 3, 20: 0, 50: 3, 100: 1, 200: 0, 500: 1, 1000: 1}), ),
#             "true_result": 1780
#         }, {

#             "message": "2. набір: {10: 0, 20: 3, 50: 1, 100: 0, 200: 0, 500: 0, 1000: 0}",
#             "func": get_sum_cost_atm, "params": (create_stack_bills({10: 0, 20: 3, 50: 1, 100: 0, 200: 0, 500: 0, 1000: 0}), ),
#             "true_result": 110
#         }, {

#             "message": "3. набір: ((10, 0), (20, 3), (50, 1), (100, 0), (200, 0), (500, 0), (1000, 0))",
#             "func": get_sum_cost_atm, "params": (create_stack_bills({10: 0, 20: 3, 50: 1, 100: 0, 200: 0, 500: 0, 1000: 0}), ),
#             "true_result": 110
#         }, {

#             "message": "4. набір: 0, 3, 1, 0, 0, 0, 0",
#             "func": get_sum_cost_atm, "params": (create_stack_bills(0, 3, 1, 0, 0, 0, 0), ),
#             "true_result": 110
#         }, {

#             "message": "5. набір: {p10=0, p20=3, p50=1, p100=0, p200=0, p500=0, p1000=0}",
#             "func": get_sum_cost_atm, "params": (create_stack_bills(p10=0, p20=3, p50=1, p100=0, p200=0, p500=0, p1000=0), ),
#             "true_result": 110
#         }, {

#             "message": "6. набір: {p20=3, p50=1}",
#             "func": get_sum_cost_atm, "params": (create_stack_bills(p20=3, p50=1), ),
#             "true_result": 110
#         }]
#     for case in cases:
#         if not case['func'](*case['params']) == case['true_result']:
#             print(f"{case['message']}: {case['func'].__name__}{case['params']}\
#  => {case['func'](*case['params'])} == {case['true_result']} : ('Error')")
#         else:
#             print(f"{case['message']} : Passed")

#         print("-"*15)

#     print("-"*45)


#     print("II. перевірка remove_non_digit_char()")
#     cases = [
#         {
#             "message": "1. Правильне число",
#             "func": remove_non_digit_char, "params": (123, ),
#             "true_result": 123
#         }, {
#             "message": "2. Правильне число рядок",
#             "func": remove_non_digit_char, "params": ("123", ),
#             "true_result": 123
#         }, {
#             "message": "3. Рядок з літерою спочатку",
#             "func": remove_non_digit_char, "params": ("b123", ),
#             "true_result": 123
#         }, {
#             "message": "3.1 Рядок з літерами спочатку",
#             "func": remove_non_digit_char, "params": ("boob123", ),
#             "true_result": 123
#         }, {
#             "message": "4. Рядок з літерою в кінці",
#             "func": remove_non_digit_char, "params": ("123а", ),
#             "true_result": 123
#         }, {
#             "message": "4.1 Рядок з літерами в кінці",
#             "func": remove_non_digit_char, "params": ("123арррра", ),
#             "true_result": 123
#         }, {
#             "message": "5. Рядок з літерою спочатку і в кінці",
#             "func": remove_non_digit_char, "params": ("e123а", ),
#             "true_result": 123
#         }, {
#             "message": "5.1 Рядок з літерами спочптку і в кінці",
#             "func": remove_non_digit_char, "params": ("lskjf123арррра", ),
#             "true_result": 123
#         }, {
#             "message": "6 Рядок з літерами та декілька груп чисел",
#             "func": remove_non_digit_char, "params": ("lf123арр458рр789а", ),
#             "true_result": 123
#         }, {
#             "message": "7 Рядок тільки з літерами",
#             "func": remove_non_digit_char, "params": ("lskjfарррра", ),
#             "true_result": 0
#         }, {
#             "message": "7 Пустий рядок",
#             "func": remove_non_digit_char, "params": ("", ),
#             "true_result": 0
#         }, {
#             "message": "8 Число текст float",
#             "func": remove_non_digit_char, "params": ("d123.56ff", ),
#             "true_result": 123
#         }
#         ]
#     for case in cases:
#         if not case['func'](*case['params']) == case['true_result']:
#             print(f"{case['message']}: {case['func'].__name__}{case['params']}\
#  => {case['func'](*case['params'])} == {case['true_result']} : ('Error')")
#             print("-"*15)
#     print("-"*45)

#     print("I. Перевірка create_stack_bills з різними видами параметрів")
#     print("1 варіант передачі позиційних параметрів")
#     result = create_stack_bills(2, 3, 4, 5, 6)
#     print(f"{result=}")
#     print("-"*15)

#     print("2 варіант передачі 1й позиційний параметр dict")
#     result = create_stack_bills(
#         {10: 3, 20: 0, 50: 23, 100: 18, 75: 4}, 2, 3, 4, 5, 6)
#     print(f"{result=}")
#     print("-"*15)

#     print("3 варіант передачі 1й позиційний параметр seq - tuple")
#     result = create_stack_bills((3, 0, 23, 18, 75), 2, 3, 4, 5, 6)
#     print(f"{result=}")
#     print("-"*15)

#     print("4 варіант передачі 1й позиційний параметр seq - list")
#     result = create_stack_bills([3, 0, 23, 18, 75], 2, 3, 4, 5, 6)
#     print(f"{result=}")
#     print("-"*15)

#     print("5 варіант передачі іменовані аргументи")
#     result = create_stack_bills(p10=2, p50=3, b200=4, f500=5, k1000=6)
#     print("-"*45)
#     print(f"{result=}")
#     print("-"*15)

#     print("6 варіант передачі Першим позиційним параметром списка виду: \
# ((key, value), ..)")
#     result = create_stack_bills(
#         (10, 2), (50, 3), (200, 4), (500, 5), (1000, 6))
#     print("-"*45)
#     print(f"{result=}")
#     print("-"*15)

#     print("6.1 варіант передачі Першим позиційним параметром списка виду: \
# ((key, value), ..) нечислові параметри")
#     result = create_stack_bills(
#         (("10fgr", 2), ("50", "3"), ("ty200r", 4), (500, "r5"), (1000, 6)))
#     print(f"{result=}")
#     print("-"*15)

#     print("7 варіант передачі Переліком позиційних параметрів списка виду: \
# (key, value), ...")
#     result = create_stack_bills(
#         (10, 2), (50, 3), (200, 4), (500, 5), (1000, 6))
#     print("-"*45)
#     print(f"{result=}")
#     print("-"*15)

#     print("7.1 варіант передачі Переліком позиційних параметрів списка \
# виду: (key, value), ... нечислові параметри")
#     result = create_stack_bills(
#         ("10fgr", 2), ("50", "3"), ("ty200r", 4), (500, "r5"), (1000, 6))
#     print(f"{result=}")
#     print("-"*15)

    # print("8 варіант передачі Пустий набір")
    # result = create_stack_bills()
    # print("-"*45)
    # print(f"{result=}")
    # print("-"*15)
