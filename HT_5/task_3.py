# task_3.py
# Написати функцию <is_prime>, яка прийматиме 1 аргумент - число від 0 до 1000, 
# і яка вертатиме True, якщо це число просте і False - якщо ні.
# 
def is_prime(value):
    """
    Функція, що визначає чи є число на проміжку 0 ... 1000 просте чи ні

    Вхідні дані: число від 0 до 1000

    Вихідні дані: Просте value (True) чи ні(False)
     або створюємо виключення якщо передане число не задовольняє вимогам
    
    Оскільки величина не дуже велика застосовувати рещшето Ератосфена 
    немає смисла, будемо просто ділити на числа від 2 до value/2  і 
    дивидись на остачу

    """
    print(f"isinstance(value, int):{isinstance(value, int)}")
    if isinstance(value, int): 
        if value > 1000 or value < 0:
            raise ValueError(f"You value: {value} is not in range 0..1000")
    else:
        raise TypeError(f"You value: {value} is not int")
    
    if value == 0:
        return False        
    if value == 1:
        return True

    for d in range(2, value // 2 + 1):
        if value % d == 0:
            return False

    return True

# Допоміжні функції
def enter_numeric_value(msg, flag_empty=False, type_cast_function=float, cnt_attemts=5):
    """
    Функція, що допомагає проводити введення даних від користувача

    Вхідні дані
     * msg - Повідмлення для пояснення вводу
     * flag_empty - признак можливості відсутності введених даних (False) - буде повернуто None
     * type_cast_function - функція приведення введених текстових даних (float)
     * cnt_attemts - кількість спроб вводу значення (5)
    
    Вихідні дані:
     * введене значення числового типу, в залежності від type_cast_function
     * None - якщо не вдалось привести до бажаного типу введене коистувачем значення,
     або якщо зведений прапорець flag_empty і дані не були введені
    """
    def remove_no_numeric_symbs(value):
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

    for attempt in range(cnt_attemts):
        print(f"Attempt {attempt + 1}. ", end=" ")
        sinp = input(msg + ": ").strip()
        value = None
        if flag_empty and sinp == "":
            return value
        
        try:
            value = type_cast_function(remove_no_numeric_symbs(sinp))
        except ValueError as ex:
            print(f"You enter wrong number: {sinp}")
            continue

        break

    return value

if __name__ == "__main__":
    test_number = enter_numeric_value("Enter int value in range 0..1000", type_cast_function=int)

    print(f"The your value: {test_number} is prime :{is_prime(test_number)}")



