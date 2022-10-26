# task_7.py
# Написати функцію, яка приймає на вхід список (через кому), 
# підраховує кількість однакових елементів у ньому і виводить результат. 
# Елементами списку можуть бути дані будь-яких типів. Наприклад:
# 1, 1, 'foo', [1, 2], True, 'foo', 1, [1, 2] ----> "1 -> 3, foo -> 2, [1, 2] -> 2, True -> 1"
# 
def count_els(s_value):
    """
    Підрахунок кількості однакових елементів у рядку

    Вхідні дані:
     * s_value - рядок для аналізу
    
    Вихідні дані:
     * видід лількості однакових елементів
    """
    # Перевірка відповідності даних
    if not isinstance(s_value, str):
        raise TypeError("Sorry your input are not a string.")
    
    print("input string:", s_value)

    tpl_bracets = (("(", ")"), ("[", "]"), ("{", "}"))
    tpl_b_bracets = tuple(map(lambda item: item[0], tpl_bracets))
    tpl_e_bracets = tuple(map(lambda item: item[1], tpl_bracets))

    for idx in range(len(tpl_bracets)):
        if s_value.count(tpl_bracets[idx][0]) != s_value.count(tpl_bracets[idx][1]):
            raise ValueError(f"In input str {s_value} count of open bracets:{tpl_bracets[idx][0]} not corresponding with close bracets: {tpl_bracets[idx][0]}")

    lst = []
    lst_keep = []
    level_ = 0

    for item in s_value:
        if level_ == 0 and item == ",": #end of element
            lst.append("".join(lst_keep).strip())
            lst_keep.clear()
            continue

        if item in tpl_b_bracets:
            level_ += 1

        if item in tpl_e_bracets:
            level_ -= 1

        lst_keep.append(item)
    lst.append("".join(lst_keep).strip())

    dct = dict()
    for item in lst:
        dct[item] = dct.get(item, 0) + 1

    out_lst = []
    for key, value in dct.items():
        out_lst.append(f"{str(key)} -> {value}")
    print(", ".join(out_lst))


def cnt_eq_list_items(seq):
    """
    Підрахунок кількості однакових елементів у списку
    В якості елементів можуть бути будь які (змінні та незмінні типи)
    Реалізувати такий підрахунок за допомогою словника неможливо, 
     набір (set) також застосувати неможливо
    """
    def get_idx(item, lst):
        """
        пошук індекса у списку елементів виду [[value, cnt], ... ] по значенню value

        return
            індекс елемента якщо його знайдено 
            -1 якщо елемен не знайдено
        """

        for idx, value in enumerate(lst):
            if value[0] == item and type(value[0]) == type(item):
                return idx

        return -1

    result = []
    for el in seq:
        idx = get_idx(el, result)
        if idx == -1: 
            # Not found
            result.append([el, 1])
        else:
            # Found
            result[idx][1] += 1

    return result

def help_quote(value):
    return "'" if isinstance(value, str) else ""

if __name__ == "__main__":
    # case 1 - String
    count_els("1, 1, 'foo', [1, 2], True, 'foo', 1, [1, 2]") # ----> "1 -> 3, foo -> 2, [1, 2] -> 2, True -> 1"
    # case 2- List
    output = []
    for item in cnt_eq_list_items([1, 1, 'foo', [1, 2], True, 'foo', 1, [1, 2]]):
        output.append(f"{help_quote(item[0])}{item[0]}{help_quote(item[0])} -> {item[1]}")
    print(", ".join(output))
