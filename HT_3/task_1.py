# task_1.py
# 1. Write a script that will run through a list of tuples and replace the last value for each tuple. 
# The list of tuples can be hardcoded. 
# The "replacement" value is entered by user. 
# The number of elements in the tuples must be different.

# Робота над помилками:
# * замінено 2ва принти на один, з f-рядком
# * обробка ситуації наявності пустого кожтежа, оскільки потрбно замінювати останній елемент, а 
# він відсутній, то в результат вставляємо пустий кортеж
# 2
# Коригування перевірки умови пустого кортежа

lst_tpls = [(1, 24, 17, "A"), (2, "B"), (3 ,45, "C"), (4, 5, 5, "D"), (5, "E"), ("F", ), ()]
print(f"Input values: {lst_tpls}")

value = input("Enter any value to replacenment: ")

lst_result = []
for tpl in lst_tpls:
    lst_t = list(tpl)
    if tpl:
        lst_t[-1] = value
    lst_result.append(tuple(lst_t))

lst_tpls = lst_result
print("-"*78)
print(f"Changed values: {lst_tpls}")
