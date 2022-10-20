# task_6.py
# Написати функцію, яка буде реалізувати логіку циклічного зсуву елементів в списку. 
# Тобто функція приймає два аргументи: 
#  * список 
#  * величину зсуву (якщо ця величина додатна - пересуваємо з кінця на початок, 
#  якщо від'ємна - навпаки - пересуваємо елементи з початку списку в його кінець). 
#  
#  Наприклад:
#   fnc([1, 2, 3, 4, 5], shift=1) --> [5, 1, 2, 3, 4]
#   fnc([1, 2, 3, 4, 5], shift=-2) --> [3, 4, 5, 1, 2]
#   
def shift_list(in_lst, shift):
    """
    Циклічний зсув списку вправо або вліво

    Вхідні дані
     * in_lst   - Списо для роботи
     * shift - Величина зсуву
    
    Вихідні дані:
     * Повернення дубльованого вхідного списка, циклічно зсунутого на shift позицій
     * Генерується виключення при передачі невідповаідних аргументів
    """
    if not isinstance(in_lst, list):
        raise TypeError(f"Transferred incorrect list: {in_lst}")
    if not type(shift) == int:
        raise TypeError(f"Transferred incorrect shift type need int, present{type(shift)}")

    real_shift = abs(shift) % len(in_lst)
    lst = list(in_lst)

    if shift == 0:
        return lst
    if shift > 0: # -->
        w_lst = []
        for _ in range(real_shift):
            w_lst.append(lst.pop())
        w_lst = w_lst[::-1]
        w_lst.extend(lst)
        return w_lst
    else: # <--
        w_lst = []
        for _ in range(real_shift):
            w_lst.append(lst.pop(0))
        lst.extend(w_lst)
        return lst

if __name__ == "__main__":
    print("fnc([1, 2, 3, 4, 5], shift=1) --> " , shift_list([1, 2, 3, 4, 5], shift=1))
    print("fnc([1, 2, 3, 4, 5], shift=-2) <-- ", shift_list([1, 2, 3, 4, 5], shift=-2))


    lst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    print("Inital list:", lst)
    print("shift=3", shift_list(lst, shift=3))

    print("Inital list:", lst)
    print("shift=-2", shift_list(lst, shift=-2))

    print("Inital list:", lst)
    print("shift=14", shift_list(lst, shift=14))

    print("Inital list:", lst)
    print("shift=-15", shift_list(lst, shift=-15))
