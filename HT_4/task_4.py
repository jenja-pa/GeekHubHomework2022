# task_4.py
# Наприклад маємо рядок --> 
# "f98neroi4nr0c3n30irn03ien3c0rfe kdno400we(nw,kowe%00koi!jn35pijnp4 6ij7k5j78p3kj546p4 65jnpoj35po6j345" -> 
#  просто потицяв по клавi =) Створіть ф-цiю, яка буде отримувати довільні 
# рядки на зразок цього та яка обробляє наступні випадки:
# 
# якщо довжина рядка в діапазоні 30-50 (включно) -> прiнтує довжину рядка, кiлькiсть букв та цифр
# якщо довжина менше 30 -> прiнтує суму всіх чисел та окремо рядок без цифр та знаків лише з буквами (без пробілів)
# якщо довжина більше 50 -> щось вигадайте самі, проявіть фантазію =)
# 

def get_user_input(msg="Please enter your value"):
    """
Getting user input 

return user input
    """
    return input(msg + ": ")

def sum_digits_and_chars(value):
    """
    довжина менше 30 -> прiнтує суму всіх чисел та окремо рядок без цифр та знаків лише з буквами (без пробілів)
    """
    my_sum = 0
    lst = []
    for ch in value:
        if ch.isdigit():
            my_sum += int(ch)
        elif ch.isalpha():
            lst.append(ch)
     
    print(f"len input LT 30: sum of digits: {my_sum}, string: {''.join(lst)}")       

def my_case(value):
    """
    довжина більше 50 -> щось вигадайте самі
    визначити у рядку всі набори наявних чисел (число - підряд ідучі цифри)
    """
    lst = []
    keep_digits = ""
    for ch in value:
        if ch.isdigit():
            keep_digits += ch
        elif len(keep_digits)>0:
            lst.append(keep_digits)
            keep_digits = ""
    if keep_digits:
        lst.append(keep_digits)
 
    print(f"len input GT 50: list of numbers: {lst}")

def len_cnt_digits_and_chars(value):
    """
    Вивести довжину рядка, кiлькiсть букв та цифр
    """
    dct = dict()
    for ch in value:
        if ch.isdigit() or ch.isalpha():
            dct[ch] = dct.get(ch, 0) + 1

    print(f"len input in range 30..50: {len(value)}. count of chars: {dct}")
def bar(value):
    """
    Функція, що обробляє отриманий рядок
    повертає повідомлення в залежності від довжини рядка
    """
    print(value, len(value))

    if len(value) < 30:
        sum_digits_and_chars(value)
    elif len(value) > 50:
        my_case(value)
    else: # range(30-50)
        len_cnt_digits_and_chars(value)

if __name__ == "__main__":
    bar(get_user_input("Enter any symbols"))