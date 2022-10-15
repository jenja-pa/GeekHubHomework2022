# task_1.py
# Написати функцiю season, яка приймає один аргумент (номер мiсяця вiд 1 
#  до 12) та яка буде повертати пору року, до якої цей мiсяць належить 
#  (зима, весна, лiто або осiнь). 
# У випадку некоректного введеного значення - виводити відповідне повідомлення.
# 

def season(n_month):
    """
    Function return name of season for number of month

    Return name of season or None if present error
    """
    result = None
    if type(n_month) == int:
        if n_month in range(1,13):
            shift_month = n_month % 12 
            n_season = shift_month // 3
            result = {0:"Winter", 1:"Spring", 2:"Summer", 3:"Autumn"}[n_season]
        else:
            print(f"Error, your enter is {n_month}, but input must be integer in range 1..12")
    else:
        print(f"You enter {n_month}. Please enter the integer value")

    return result

if __name__ == "__main__":
    # simple test 
    print("Before the action, we execute simple tests:")
    assert season(1) ==  "Winter", "Error call: season(1). Fail must be Winter"
    assert season(4) == "Spring", "Error call: season(4). Fail must be Spring"
    assert season(8) == "Summer", "Error call: season(8). Fail must be Summer"
    assert season(9) == "Autumn", "Error call: season(9). Fail must be Autumn"
    assert season(12) == "Winter", "Error call: season(12). Fail must be Winter"
    assert season(0) is None, "Error call: season(0). Fail must be None"
    assert season(-2) is None, "Error call: season. Fail must be None"
    assert season(13) is None, "Error call: season. Fail must be None"
    assert season("2") is None, "Error call: season. Fail must be None"
    assert season((10,)) is None, "Error call: season. Fail must be None"
    assert season([]) is None, "Error call: season. Fail must be None"
    assert season({}) is None, "Error call: season. Fail must be None"
    assert season({"month":7}) is None, "Error call: season. Fail must be None"
    assert season(False) is None, "Error call: season. Fail must be None"
    assert season(None) is None, "Error call: season. Fail must be None"
    print("-" * 78, "\n")

    sn_month = input("Enter number of month: ")
    try:
        print(f"The season of {sn_month} month is {season(int(sn_month))}")
    except ValueError as ex:
        season(sn_month)