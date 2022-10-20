# test_4.py
# Написати функцію <prime_list>, яка прийматиме 2 аргументи - початок і кінець діапазона, 
#  і вертатиме список простих чисел всередині цього діапазона. 
# Не забудьте про перевірку на валідність введених даних та у випадку
#  невідповідності - виведіть повідомлення.
import time



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
    if not isinstance(value, int): 
        raise TypeError(f"You value: {value} is not int")
    
    if value == 0:
        return False        
    if value == 1:
        return True

    for d in range(2, value // 2 + 1):
        if value % d == 0:
            return False

    return True

def prime_list1(beg_range, end_range):
    """
    Функція, що повертає список простих чисел в межах діапазону
    1-й варіант обраховуємо прості числа методом аналізу остачі
    для цього використаємо ф-ю форроблену в завданні 3

    Вхідні дані:
     * beg_range, end_rapge - граничні значення діапазону
    
    Вихідні дані:
     * список наявних простих чисел діапазону

    """
    lst = []
    for n in range(beg_range, end_range + 1):
        if is_prime(n):
            lst.append(n)
            # print(f"{n}, ", end="")
    return lst

def prime_list2(beg_range, end_range):
    """
    Функція, що повертає список простих чисел в межах діапазону
    2-й варіант використовуємо алгоритм решето ератосфена

    Вхідні дані:
     * beg_range, end_rapge - граничні значення діапазону
    
    Вихідні дані:
     * список наявних простих чисел діапазону
    """
    lst = list(range(2, end_range + 1)) 
    for n in lst:
        if n != 0:
            for candidate in range(2 * n, end_range + 1, n):
                lst[candidate - 2] = 0    

    # filter 0 in result list
    lst = list(filter(lambda x: x != 0 and x > beg_range, lst))
    return lst

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

    beg_limit = enter_numeric_value("Enter Begin limit for generate Primary numbers", type_cast_function=int)
    if beg_limit is None:
        raise ValueError("You did not enter the correct number.")
    if beg_limit < 1:
        raise ValueError("Limit must be greater than 0")

    end_limit = enter_numeric_value("Enter End limit for generate Primary numbers", type_cast_function=int)
    if end_limit is None:
        raise ValueError("You did not enter the correct number.")
    if end_limit < 1:
        raise ValueError("Limit must be greater than 0")
    if beg_limit > end_limit:
        raise ValueError("End limit mast be greater thet begin limit")

    range_gen = (beg_limit, end_limit)
    # range_gen = (100, 10000)

    print(f"Current range to generate prime: {range_gen}")
    start = time.time()
    print("Begin execute simple prime test: Case 1")
    # print(prime_list1(*range_gen))
    prime_list1(*range_gen)
    end = time.time()
    print(f"End execute. Spent: {end - start} seconds")

    start = time.time()
    print("Begin execute Eratosfen prime test: Case 2")
    # print(prime_list2(*range_gen))
    prime_list2(*range_gen)
    end = time.time()
    print(f"End execute. Spent: {end - start} seconds")
    print("For see list of prime uncoment execute with print statement")

