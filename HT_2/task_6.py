# task_6.py
# Write a script to check whether a value from user input is contained in a group of values. 
# Напишіть срипт щоб перевірити значення вводу користувача на входження його в деяку групу значень
# e.g. 
# [1, 2, 'u', 'a', 4, True] --> 2 --> True 
# [1, 2, 'u', 'a', 4, True] --> 5 --> False
# 
#  Проблема написання скрипта у тому, що потрібно, приблизно, визначити якого типу дані вводив 
# користувач я вирішив, що присутність " чи ' на початку та в кінці рядка вводу буде вказувати 
# на точно символьні дані, при чому кількість лапок не контролюється, для простоти, всі інші 
# вводи будуть пробуватись по характерним признакам приводитись до відповідних типів. 
# Якщо привести не вдалося - то вважаємо таке значення рядком

# hardcoded values needs template
template_list = [1, 2, 'u', 'a', 4, True]
print(f"{template_list=}")

input_ = input("Enter your value (string value must be in quote or apos):").strip()
type_ = "str"

if (input_.startswith("'") and input_.endswith("'")) or (input_.startswith('"') and input_.endswith('"')): # exactly str
	value = input_.strip("'").strip('"')
elif input_.upper() in ("TRUE", "FALSE"): # bool
	value = True if input_.upper() == "TRUE" else False
	type_ ="bool"
elif input_.count(".") == 1: # float
	value = float(input_)
	type_ ="float"
elif input_.isnumeric(): # int
	value = int(input_)
	type_ ="int"
else:
	value = input_

print(f"Enter value: '{input_}', me to determine that is type: {type_}")

if value in template_list:
	print(f"You enter value: {value} ({type_}) this value is present in template_list. --> True")
else:
	print(f"You enter value: {value} ({type_}) this value is not present in template_list. --> False")
