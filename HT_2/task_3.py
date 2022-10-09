"""
task_3.py

Write a script which accepts a from user and print out a sum of the first positive integers.
Напишіть скрипт котрий приймає від користувача і друкує суму перших позитивних цілих чисел.
Уточнення:
  Вводимо число.. Наприклад 5. Виводимо суму перших 5 додатніх чисел - 1+2+3+4+5. 
  Число вводить користувач, скрипт повертає суму.
"""

sinp = input("Enter positive integer number: ").strip()
if sinp.isnumeric():
	num = int(sinp)
	sum_ = 0
	lst = []
	for item in range(num):
		sum_ += (item + 1)
		lst.append(str(item + 1))
	print(f"Result: Sum of {sinp} first positive number {'+'.join(lst)} = {sum_}")
else:
	print("Please, next enter positive integer number.")
