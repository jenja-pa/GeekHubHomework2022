# task_2.py
# Написати функцію, яка працює за наступною логікою: 
#  користувач робить вклад у розмірі одиниць строком на років під 
#  відсотків (кожен рік сума вкладу збільшується на цей відсоток, 
#  ці гроші додаються до суми вкладу і в наступному році на них 
#  також нараховуються відсотки). Параметр є необов'язковим і має 
#  значення по замовчуванню <10> (10%). 
# Функція повинна принтануть суму, яка буде на рахунку, 
#  а також її повернути (але округлену до копійок).
 
def deposit(start_amount, cnt_years, interest = 10.0):
    """
    Функція, що розраховує та динаміку зміни йог вкладу на депозиті

    Вхідні дані:
     start_amount - Початкова сума
     cnt_years - кількість років строку вкладу
     interest  - відсотки що нараховуються за рік (по замовчуванню: 10)

    Результат:
     * Вивід на екран динаміки зміни початкової суми
     * Сума вкладу на кінець періоду
    """
    start_period = start_amount
    print("# year | start value | end value")
    print("-" * 30)
    for n_year in range(cnt_years):
        end_period = round(start_period + start_period * (interest / 100.0), 2)
        print(f"{n_year + 1:6} | {start_period:11.2f} | {end_period:.2f}")
        start_period = end_period
    print("-" * 30)


    print(f"You earned for you start_amount:{start_amount:.2f} on {cnt_years:3} years, for {interest:.2f}% are {start_period - start_amount:.2f}")
    return start_period


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
    try :
        # Введення значення "Величина початкового вкладу"
        start_amount = enter_numeric_value("Enter the initial deposit amount (number)", float)

        if start_amount is None:
            raise TypeError(f"You do not enter right initial deposit amount, entered {start_amount}")
        elif start_amount <= 0.0:
            raise ValueError(f"Initial deposit amount must be larger zero, entered {start_amount}")

        # Введення значення "Кількість років"
        cnt_years = enter_numeric_value("Enter the number of years of deposit storage (number(int))", type_cast_function=int)
        if cnt_years is None:
            raise TypeError(f"You do not enter right the number of years of deposit storage, entered {cnt_years}")
        elif cnt_years == 0:
            raise ValueError(f"Number of years of deposit storage must be larger zero, entered {cnt_years}")

        # Введення відсотків
        interest = enter_numeric_value("Enter the interest of deposit storage (number(default: 10.0))", flag_empty=True)
        if interest is not None and interest <= 0:
            raise ValueError(f"Value of interest must be larger zero, entered {interest}")

        #General work procesing data
        if interest is None:
            print(f"End value of deposit is: {deposit(start_amount, cnt_years):.2f}")
        else:            
            print(f"End value of deposit is: {deposit(start_amount, cnt_years, interest):.2f}")

    except TypeError as ex:
        print(f"Sorry you entered value have a trouble. {ex}")
    except ValueError as ex:
        print(f"Sorry you entered numeric value have a trouble. {ex}")

