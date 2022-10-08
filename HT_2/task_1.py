"""
task_1.py
1. Write a script which accepts a sequence of comma-separated numbers from user and generates a list 
and a tuple with those numbers.
  Написати скрипт котрий приймає послідовність розділених комами чисел від користувача і 
створює список та кортеж цих чисел
"""

s = input("Enter a sequence of comma-separated numbers: ")
lst = s.split(",")

if len(lst) > 0:
	lst_res = []
	for el in lst:
		if el.isnumeric():
			lst_res.append(int(el))
	tpl_res = tuple(lst_res)
	print(f" list: {lst_res}")
	print(f"tuple: {tpl_res}")
else:
	print("You have not enter coma-separated sequence.")