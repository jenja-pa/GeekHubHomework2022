# task_6.py
# Write a script to get the maximum and minimum VALUE in a dictionary.
# 
# # Робота над помилками:
# * замінено два принти на один, з f-рядком
# * дійсно в попередньому варіанті забув, що існують спеціальні 
# вбудовані функції пошуку max та min

dct = {1: 1, 2:2, 3:1, 4:1, 5:2, 6:3, 7:1, 8:4, 9:2}
print(f"Input: {dct=}")
print(f" values: {', '.join(map(str, dct.values()))}")

print("-"*78)
print(f"Max value of dict: {max(dct.values())}")
print(f"Min value of dict: {min(dct.values())}")

