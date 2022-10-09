"""
task_4.py

Write a script which accepts a from user and then times asks user for string input. 
At the end script must print out result of concatenating all strings.

Написати скрипт який приймає число, від користувача - n, та вводить n раз рядок від користувача.
Після закінчення вводу вивести результат - об'єднаний рядок всих введених рядків.
Об'єдняти більш всього через пробіл 
"""

sn = input("Enter positive number: ")
if sn.isnumeric():
	lst = []
	for i in range(int(sn)):
		lst.append(input(f"{i+1:4}:"))
	print(f"\nresult concatenate:\n{' '.join(lst)}")
else:
	print("Please next enter positive number.")