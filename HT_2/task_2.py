"""
task_2.py

2. Write a script which accepts two sequences of comma-separated colors from user. 
Then print out a set containing all the colors from color_list_1 which are 
not present in color_list_2.

Написати скрипт який приймає дві розділені комою послідовності кольорів від користувача.
Тоді вивести множину яка містить всі колори із color_list_1 котрі не присутні в 
color_list_2
"""
# Закоментовано рядки що допомагали відладці
# import sys
# from io import StringIO

# oldstdin = sys.stdin
# inp_s1 = "red, blue, green, purple, yellow, pink, #f60, black, white"
# inp_s2 = "orange, purple, violet, pink, #f60, black, white-snow"

# # inp_s1 = "#f2fa51,#6e6c62,#348e1c,#dbe601,#d416ff,#3985e3,#6cb051,#fc2ba4,#4a694c,#d06c51,#b2f1d6,#4fd179,#6a04b0,#fac638,#08aaa3,#33bef0,#1f5c38,#16c1fe,#a0cbd9,#067cf7,#7e5344,#d2d26a"
# # inp_s2 = "#164d5e,#5882d3,#1597fc,#6da6fe,#0bcbd5,#34f078,#19ebe2,#9bdba5,#01acc0,#48d396,#b57a81,#1bc2b3,#e7df76,#0dd6ed,#6ec02a,#3f2d5f,#204224,#fee873,#a5e56b,#c7190f,#298ebd,#537d67"

# # inp_s1 = "#e5aa10,#1b2a7c,#89fe58,#8d4ade,#3face6,#fcce7c,#bb3fd6,#be48b5,#74ccb7,#8491aa"
# # inp_s2 = "#14f5ae,#6a5fca,#4f6269,#c3305f,#ec156f,#421df7,#398057,#3face6,#fcce7c,#cdf416,#ede9da,#4c4979,#e1948c"

# sys.stdin = StringIO(f"{inp_s1}\n{inp_s2}")

s1 = input("First values: ")
s2 = input("Second values: ")

set1 = set()
for el in s1.split(","):
	set1.add(el.strip())
set2 = set()
for el in s2.split(","):
	set2.add(el.strip())
print()
print(f"{set1=}")
print(f"{set2=}")

#out result
print("="*50)
print(f"result (set1 - set2): {set1.difference(set2)}") 

# sys.stdin = oldstdin