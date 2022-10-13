# task_5.py
# Write a script to remove values duplicates from dictionary. Feel free to hardcode your dictionary.
# 
# # Робота над помилками:
# * замінено два принти на один, з f-рядком
# * попередній варант пердбачав повернення словника з вилученими елементами значення яких
# дублюється, а потрібно було отримати тільки унікальні значення.

dct = {1: 1, 2:2, 3:1, 4:1, 5:2, 6:3, 7:1, 8:4, 9:2}
print(f"Input dict: {dct}")
print(f"Input values: {tuple(dct.values())}")
print("-"*78)
print(f"Unique values: {tuple(set(dct.values()))}")
