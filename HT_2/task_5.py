# task_5.py
# 
# Write a script which accepts a decimal number from user and converts it to hexadecimal.
# 
# Написати скрипт котрий приймає десяткове число (ціле) та конвертує його в шіснадцяткове

sn = input("Enter decimal integer positive number: ")
if sn.isnumeric():
	n = int(sn)
	print(f"result: you enter decimal: {sn.strip()} this is hex: {hex(n):s}")
else:
	print("Error!, Sorry next enter decimal integer positive number.")