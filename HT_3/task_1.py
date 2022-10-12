# task_1.py
# 1. Write a script that will run through a list of tuples and replace the last value for each tuple. 
# The list of tuples can be hardcoded. 
# The "replacement" value is entered by user. 
# The number of elements in the tuples must be different.

lst_tpls = [(1, 24, 17, "A"), (2, "B"), (3 ,45, "C"), (4, 5, 5, "D"), (5, "E"), ("F", )]
print("Input values:")
print(lst_tpls)

value = input("Enter any value to replacenment: ")

lst_result = []
for tpl in lst_tpls:
    lst_t = list(tpl)
    lst_t[-1] = value
    lst_result.append(tuple(lst_t))

lst_tpls = lst_result
print("-"*78)
print("Changed values:")
print(lst_tpls)
