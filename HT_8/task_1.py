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

def traffic_lights(seconds=25):
    """
    Емуляція світлофора для авто і пішоходів

    Кожну секунду виводити поточний стан світлофора для авто та пішоходів

    Вхідні дані:
     - seconds - кількість секунд емуляції, 
        якщо None - безкінечний цикл
    Вихідні дані:
        Вивід стану не консоль
    """

    # Список станів (авто., піш., час дії)
    lst_states = [
        ("red", "green", 4),
        ("yellow", "red", 2),
        ("green", "red", 4) 
    ]
    CNT_STATES = len(lst_states)
    
    # test parameter
    if not isinstance(seconds, int):
        raise TypeError("Your seconds parameter must be int")
    seconds = int(seconds)
    if seconds < 3:
        raise ValueError("Your parameter seconds must be 3 or more")

    phase = 0
    len_time = len(str(seconds))
    cur_tick = lst_states[phase][2]
    print(f"n tick|{'Auto':<15} {'Pedestrian':>15}")
    for sec in range(seconds):
        print(f"{sec:>6}|{lst_states[phase][0]:<15} {lst_states[phase][1]:>15}")
        sleep(1)
        cur_tick -= 1
        if cur_tick == 0:
            phase = (phase + 1) % CNT_STATES
            cur_tick = lst_states[phase][2]



if __name__ == "__main__":
    seconds = 25
    for attempt in range(5):
        try:
            tmp = input("Enter count of time in second(int) for emulation (def. 25)")
            seconds = int(tmp)
        except ValueError as ex: 
            if len(tmp) == 0:
                break
            continue
        break

    traffic_lights(seconds)



