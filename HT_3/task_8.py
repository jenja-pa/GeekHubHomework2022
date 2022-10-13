# task_8.py
# Створити цикл від 0 до ... (вводиться користувачем). 
# В циклі створити умову, яка буде виводити поточне значення, якщо 
# остача від ділення на 17 дорівнює 0.
# 
# Робота над помилками:
# * Видалено одне із обмеженнь на мінімальне значення, що може ввести
# користувач

try:
    n = int(input("Enter positive integer number: "))
    if n < 0 :
        raise ValueError

    print(f"Numbers which is shared entirely by 17 in range 0 .. {n}")
    for n in range(n + 1):
        if n % 17 == 0:
            print(n)

except ValueError as e:
    print("Error. Please next enter a correct number.")