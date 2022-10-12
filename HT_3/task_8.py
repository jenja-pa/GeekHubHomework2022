# task_8.py
# Створити цикл від 0 до ... (вводиться користувачем). 
# В циклі створити умову, яка буде виводити поточне значення, якщо остача від ділення на 17 дорівнює 0.
# 

try:
    n = int(input("Enter positive integer number larger 17: "))
    if n < 0 or n < 17:
        raise ValueError

    print("Numbers which is shared entirely by 17")
    for n in range(n + 1):
        if n % 17 == 0:
            print(n)

except ValueError as e:
    print("Error. Please next enter a correct number.")