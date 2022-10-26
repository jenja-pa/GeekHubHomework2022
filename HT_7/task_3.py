# task_3.py
# 3. Всі ви знаєте таку функцію як <range>. 
# Напишіть свою реалізацію цієї функції. 
# Тобто щоб її можна було використати у вигляді:
    # for i in my_range(1, 10, 2):
    #     print(i)
    # 1
    # 3
    # 5
    # 7
    # 9
# P.S. Повинен вертатись генератор.
# P.P.S. Для повного розуміння цієї функції - можна почитати документацію по ній: 
# https://docs.python.org/3/library/stdtypes.html#range
# P.P.P.S Не забудьте обробляти невалідні ситуації (типу range(1, -10, 5) тощо). 
# Подивіться як веде себе стандартний range в таких випадках.

def my_range(*args):
    """
    моя реалізація функції генератора range(stop) абл range(start, stop, step=1)

    Приймає 1, 2 чи 3 аргументи
    Аргументи тільки цілі числа
    Якщо 1 арг. ш він == 0 -> пуста послідовність
    Якщо 2ва арг. та 1й арг.(start) >= 2гого арг.(stop) -> пуста послідовність
    Якщо всі обмеження задоволені:
     Формується Висхідна (step>0) або Нисхідна (step<0) послідовність
    """
    if len(args) == 0:
        raise TypeError("range expected at least 1 argument, got 0")
    
    for item in args:
        if not isinstance(item, int):
            raise TypeError(f"'{type(item).__name__}' object cannot be interpreted as an integer")

    if len(args) == 1:
        start = 0
        stop = args[0]
        if stop == 0:
            return ()
        step = 1
    elif len(args) == 2:
        start = args[0]
        stop = args[1]
        if start >= stop:
            return ()
        step = 1
    elif len(args) == 3:
        start = args[0]
        stop = args[1]
        step = args[2]
        if step == 0:
            raise ValueError("range() arg 3 must not be zero")
    else:
        raise TypeError(f"range expected at most 3 arguments, got {len(args)}")

    if step > 0: #Positive step^ r[i] = start + step*i where i >= 0 and r[i] < stop
        current = start
        while current < stop:
            yield current
            current += step
    else: #Negative step:  r[i] = start + step*i, but the constraints are i >= 0 and r[i] > stop.
        current = start
        while current > stop:
            yield current
            current -= abs(step)


if __name__ == "__main__":
    # range expected at least 1 argument, got 0
    # print(tuple(my_range()))
    
    #parameter -  object cannot be interpreted as an integer
    # print(tuple(my_range("1")))
    # print(tuple(my_range(0, 12.0, 1)))
    # print(tuple(my_range(2, 12, "4")))
    
    # pass 0 - return empty generator
    print(tuple(my_range(0)))

    # pass start greater by stop - return empty generator
    print(tuple(my_range(12, 5)))
    print(tuple(my_range(1, 0)))

    # pass step == 0, Exception
    # print(tuple(my_range(2, 15, 0)))

    # pass more than 3 parameters - Exception    
    # print(tuple(my_range(2, 15, 0, 4, 6)))

    # good parameters
    # Positive step
    print("Positive Step")
    print(tuple(my_range(2, 15, 2)))

    # Negative step
    print("Negative Step")
    print(tuple(my_range(0, -10, -1)))

    # Збійна ситуація
    print("Error case")
    print(tuple(my_range(1, -10, 5)))

