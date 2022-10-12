# task_5.py
# Write a script to remove values duplicates from dictionary. Feel free to hardcode your dictionary.
# 

dct = {1: 1, 2:2, 3:1, 4:1, 5:2, 6:3, 7:1, 8:4, 9:2}
print("Input:")
print(f"{dct=}")

lst = []
dct_result = dict()
for key, val in dct.items():
    if not val in lst:
        lst.append(val)
        dct_result[key] = val

print("-"*78)
print("After delete duplicate values:")
print(f"{dct_result=}")
