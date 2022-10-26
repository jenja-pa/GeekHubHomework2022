# task_4.py
# 4. Реалізуйте генератор, який приймає на вхід будь-яку ітерабельну послідовність 
# (рядок, список, кортеж) і повертає генератор, який буде повертати значення з цієї 
# послідовності, при цьому, якщо було повернено останній елемент із послідовності - 
# ітерація починається знову.
   # Приклад (якщо запустили його у себе - натисніть Ctrl+C ;) ):
   # for elem in my_generator([1, 2, 3]):
   #     print(elem)
   # 1
   # 2
   # 3
   # 1
   # 2
   # 3
   # 1
   # .......

def my_cycle_generator(seq):
    try:
        iterator = iter(seq)
    except TypeError:
        raise TypeError(f"function: my_cycle_generator: Sorry you pass not iterable value: {seq}")

    while True:
        for item in seq:
            yield item 


# if __name__ == "__main__":
    # for elem in my_cycle_generator([1, 2, 3]):
    #     print(elem)

    # for elem in my_cycle_generator("[1,2,3]"):
    #     print(elem)

    # for elem in my_cycle_generator(("ab", "boo", 3)):
    #     print(elem)

    # Exception
    # for elem in my_cycle_generator(345):
    #     print(elem)
