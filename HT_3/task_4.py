# task_4.py
# Write a script that combines three dictionaries by updating 
#  the FIRST one (you can use dicts from the previous task).
  
print("Input values:")
dict_1 = {'foo': 'bar', 'bar': 'buz'} 
dict_2 = {'dou': 'jones', 'USD': 36} 
dict_3 = {'AUD': 19.2, 'name': 'Tom'}
print(f"{dict_1=}")
print(f"{dict_2=}")
print(f"{dict_3=}")

dict_1.update(dict_2)
dict_1.update(dict_3)

print("Result")
print(f"{dict_1=}")
