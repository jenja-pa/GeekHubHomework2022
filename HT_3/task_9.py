# task_9.py
# Користувачем вводиться початковий і кінцевий рік. 
# Створити цикл, який виведе всі високосні роки в цьому проміжку (границі включно). 
# P.S. Рік є високосним, якщо він кратний 4, але не кратний 100, а також якщо він кратний 400.
# 

try:
    b_year = int(input("Enter begin year (positive number): "))
    e_year = int(input("Enter end year (positive number, larger by begin year): "))
    if b_year < 0 or e_year < b_year:
        raise ValueError

    print("List of leap years:")
    for y in range(b_year, e_year + 1):
        if (y % 4 ==0 and not(y % 100 == 0)) or y % 400 == 0:
            print(y)

except ValueError as e:
    print("Error. Please next enter a correct values.")