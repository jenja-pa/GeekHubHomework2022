# task_7.py
# Write a script which accepts a (int) from user and generates 
#  dictionary in range where key is and value is
#  * e.g. 3 --> {0: 0, 1: 1, 2: 4, 3: 9}
#  
# # Робота над помилками:
# * замінено два принти на один, з f-рядком
# * зкориговано = int(idx ** 2), на = idx * idx, приведення типу було 
# потрібне оскільки піднесення у степінь повертає float, але в даному 
# випадку ця операція дійсно непідходящий варіант використання
# 
dct = dict()

try:
    n = int(input("Enter positive integer number: "))
    if n < 0:
        raise ValueError
    for idx in range(n + 1):
        dct[idx] = idx * idx
    print("-"*78)
    print(f"Result: {dct}")
except ValueError as e:
    print("Error. Please next enter a correct number.")



