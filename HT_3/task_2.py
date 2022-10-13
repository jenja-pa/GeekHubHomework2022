# task_2.py
# 2. Write a script to remove empty elements from a list.
# Test list: [(), ('hey'), ('',), ('ma', 'ke', 'my'), [''], {}, ['d', 'a', 'y'], '', []]
# 
# # Робота над помилками:
# * замінено два принти на один, з f-рядком

lst = [(), ('hey'), ('',), ('ma', 'ke', 'my'), [''], {}, ['d', 'a', 'y'], '', []]
print(f"Input data: {lst}")

lst_result = []
for item in lst:
    if item:
        lst_result.append(item)

print("-"*78)
print(f"Result:(removed empty elements){lst_result}")
