# task_7.py
# 7. Напишіть функцію, яка приймає 2 списки. 
# Результатом має бути новий список, в якому знаходяться елементи першого списку, 
# яких немає в другому. 
# Порядок елементів, що залишилися має відповідати порядку в першому (оригінальному)
#  списку. 
# Реалізуйте обчислення за допомогою генератора в один рядок.
#     Приклад:
#     array_diff([1, 2], [1]) --> [2]
#     array_diff([1, 2, 2, 2, 3, 4], [2]) --> [1, 3, 4] (edited) 

def array_diff(seq1, seq2):
    """
    Формування списку елементів seq1 яких немаж у seq2
    """
    return [item for item in seq1 if item not in seq2]


# if __name__ == "__main__":
#     print(array_diff([1, 2], [1]))
#     print(array_diff([1, 2, 2, 2, 3, 4], [2]))

#     print(array_diff(["Velit", "laboris", "dolor", "laborum", "in", "voluptate", "officia", "ut exercitation", 
#         "in dolor", "consectetur", "consequat", "id"], ["Lorem", "dolor", "laborum", "in", "id"]))