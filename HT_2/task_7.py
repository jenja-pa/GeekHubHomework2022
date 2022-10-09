# task_7.py
# 
# 7. Write a script to concatenate all elements in a list into a string and print it. 
# List must include both strings and integers and must be hardcoded.
# 
# Написати скрипт який перетворить список у рядок та виведе його.
# Список повинен містити рядки та цілі числа і повиннен бути жорстко закодований.

lst = [
	  "Lorem", 12, "ipsum", "dolor", 25, "sit", "amet,", "vel", 65, "an", "summo", "impedit.", 
	  "Ad", 18, "enim", "vivendo", 349, "pro,", "quo", "utroque", 11, 17, 345, "percipitur", 
	  "inciderint", 28, "ex,", "cu", "dolorum", 67, "conceptam", "expetendis", "nam."
	  ]
print("Input data:")
print(lst)
print("-"*70)

res = []
for item in lst:
	res.append(str(item))

print("Result:")
print(" ".join(res))
