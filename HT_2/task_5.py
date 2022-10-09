# task_5.py
# 
# Write a script which accepts a decimal number from user and converts it to hexadecimal.
# 
# Написати скрипт котрий приймає десяткове число (ціле) та конвертує його в шіснадцяткове

DCT_CONVERT = {0:"0", 1:"1", 2:"2", 3:"3", 4:"4", 5:"5", 6:"6", 7:"7", 8:"8", 9:"9", 
		10:"a", 11:"b", 12:"c", 13:"d", 14:"e", 15:"f"}

sn = input("Enter decimal integer positive number: ")
if sn.isnumeric():
	n = int(sn)
	if n == 0:
		print(f"result: you enter decimal: 0 this is hex 0x0")	
		exit()
	lst = []
	while n > 0:
		lst.append(DCT_CONVERT[n % 16])
		n //= 16
	lst = lst[::-1]
	print(f"result: you enter decimal: {sn.strip()} this is hex 0x{''.join(lst)}")
else:
	print("Error!, Sorry next enter decimal integer positive number.")