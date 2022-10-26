# task_6.py
# 6. Напишіть функцію,яка приймає рядок з декількох слів і повертає довжину 
# найкоротшого слова. Реалізуйте обчислення за допомогою генератора в один рядок.

def len_shortest_word(value):
    """
    Однорядкова функція обчислення довжини самого короткого слова у фразі

    Return:
     довжина самого короткого слова
    """
    if not isinstance(value, str):
        raise TypeError("Value must be a string")
    return min([len(item) for item in value.split()])

if __name__ == "__main__":
    print(len_shortest_word("Lorem ipsum sint consectetur eiusmod nostrud occaecat anim sit adipisicing voluptate cillum sit nulla deserunt qui"))
    print(len_shortest_word("Aliquip consequat infbor"))
    print(len_shortest_word("Eiusmod nostrud animw reprehenderit consectetur laboris autte duis nostrud tempor officia est proident voluptate fugiat magna"))
    print(len_shortest_word("Eiusmod ex reprehenderit laborum reprehenderit id enim culpa irure veniam"))



