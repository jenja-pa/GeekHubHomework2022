# task_5.py
# Написати функцію <fibonacci>, яка приймає один аргумент і виводить всі 
#  числа Фібоначчі, що не перевищують його.
#  

def fibonacci(value):
    """
    Виведення чисел фібоначі які менше вказаного значення

    Вхідні дані:
     * value - граничне значення 
    
    Вихідні дані:
     * видід чисел фібонаці менших за value
    """
    print(f"Fibonacci number less than {value}:")
    n__2 = 0
    n__1 = 1
    print(f"{n__2}, {n__1}", end="")
    while  n__2 + n__1 < value:
        n__2, n__1 = n__1, n__1 + n__2
        print(f", {n__1}", end="")


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
    
    limit = enter_numeric_value("Enter limit for generate Fibonacci numbers", type_cast_function=int)

    if limit is None:
        raise ValueError("You did not enter the correct number.")
    if limit <= 1:
        raise ValueError("Limit must be greater than 1")
    
    fibonacci(limit)
