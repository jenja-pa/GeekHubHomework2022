# task_3.py
# Write a script to concatenate the following dictionaries to create a NEW one. 
# dict_1 = {'foo': 'bar', 'bar': 'buz'} 
# dict_2 = {'dou': 'jones', 'USD': 36} 
# dict_3 = {'AUD': 19.2, 'name': 'Tom'}

dict_1 = {'foo': 'bar', 'bar': 'buz'} 
dict_2 = {'dou': 'jones', 'USD': 36} 
dict_3 = {'AUD': 19.2, 'name': 'Tom'}

dct = dict()
dct.update(dict_1)
dct.update(dict_2)
dct.update(dict_3)

print(dct)