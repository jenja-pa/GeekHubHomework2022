# task_2.py
# 2. Write a script to remove empty elements from a list.
# Test list: [(), ('hey'), ('',), ('ma', 'ke', 'my'), [''], {}, ['d', 'a', 'y'], '', []]
# 
lst = [(), ('hey'), ('',), ('ma', 'ke', 'my'), [''], {}, ['d', 'a', 'y'], '', []]
print("Input data:")
print(lst)

lst_result = []
for item in lst:
    if item:
        lst_result.append(item)

print("-"*78)
print("Result:(removed empty elements)")
print(lst_result)