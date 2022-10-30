# task_1.py
# 1. Програма-світлофор.

   # Створити програму-емулятор світлофора для авто і пішоходів. 
   
   # Після запуска програми на екран виводиться в лівій половині - 
   #  колір автомобільного, а в правій - пішохідного світлофора.    
   # Кожну 1 секунду виводиться поточні кольори.    
   #  Через декілька ітерацій - відбувається зміна кольорів - логіка така 
   #  сама як і в звичайних світлофорах (пішоходам зелений тільки коли 
   # автомобілям червоний).
   
   # Приблизний результат роботи наступний:
      # Red        Green
      # Red        Green
      # Red        Green
      # Red        Green
      # Yellow     Red
      # Yellow     Red
      # Green      Red
      # Green      Red
      # Green      Red
      # Green      Red
      # Yellow     Red
      # Yellow     Red
      # Red        Green
from time import sleep
import sys
import os
import shutil

def my_align(value, width):
    spaces = width - len(str(value))
    return str(value) + " " * spaces

# Список станів (авто., піш., час дії)
lst_states = [
    ("Red", "Green", 4),
    ("Yellow", "Red", 2),
    ("Green", "Red", 4) 
]
CNT_STATES = len(lst_states)

os.system('cls' if os.name=='nt' else 'clear')

width, _ = shutil.get_terminal_size()
width_2 = width // 2


phase = 0
cur_tick = lst_states[phase][2]
while True:
# for sec in ange(seconds):
    try:
        print(f"{my_align(lst_states[phase][0], width_2)}{my_align(lst_states[phase][1], width_2)}")
        sleep(1)
        cur_tick -= 1
        if cur_tick == 0:
            phase = (phase + 1) % CNT_STATES
            cur_tick = lst_states[phase][2]        
    except KeyboardInterrupt as ex:
        break




