# task_6.py
# Write a script to get the maximum and minimum VALUE in a dictionary.
# 

dct = {1: 1, 2:2, 3:1, 4:1, 5:2, 6:3, 7:1, 8:4, 9:2}
print("Input:")
print(f"{dct=}")
print(" values:", end=" ")
print(", ".join(map(str, dct.values())))

max_val = None
for el in dct.values():
    max_val = el
    break
min_val = max_val

for val in dct.values():
    if max_val < val:
        max_val = val
    if min_val > val:
        min_val = val

print("-"*78)
print(f"Max value of dict: {max_val}")
print(f"Min value of dict: {min_val}")

