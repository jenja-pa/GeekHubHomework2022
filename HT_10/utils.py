"""
utils.py

Модуль з утилітами які використовуються в роботі

"""
import os
import sys
import shutil
from itertools import chain as it_chain, count as it_count


def wait_key(message="Press any key ..."):
    ''' 
    function - getch()
    Wait for a key press on the console and return it. 
    '''
    result = None
    if message is not None:
        print(message)
    if os.name == 'nt':
        import msvcrt
        result = msvcrt.getwch()
    else:
        import termios
        fd = sys.stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        try:
            result = sys.stdin.read(1)
        except IOError:
            pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)

    return result


class NameIncorrectException(Exception):
    """
    Виключна ситуація - неправильне ім'я користувача
    """


class PasswordIncorrectException(Exception):
    """
    Виключна ситуація - неправильне ім'я користувача
    """
  
# Ф-ія перевіркм правил задання імені та пароля
def validations_name_password(name, pwd):
    """
    Перевірка валідності пари:
    * name     - Ім'я (літери числа не починається із числа білье 3х символів)
    * pwd      - Пароль (довше 8ми, повинна бути хоч одна літера ниж. та ВЕРХ.
     регістру і цифра)

    Return:
        True    - Якщо параметри задовільняють вимогам
        Exception   - якщо маємо проблеми
    """
    digits = (*map(str, range(10)), )
    lower_lets = (*map(chr, (el for el in range(ord('a'), ord("z")+1))), )
    upper_lets = (*map(chr, (el for el in range(ord('A'), ord("Z")+1))), )
    service_name_chars = ("_", "-")
    service_pwd_chars = ("_", )

    valid_name_chars = (*digits, *lower_lets, *upper_lets, *service_name_chars)
    valid_pwd_chars = (*digits, *lower_lets, *upper_lets, *service_pwd_chars)

    if len(name) < 3:
        raise NameIncorrectException(f"Your name '{name}' is short")
    if len(name) > 50:
        raise NameIncorrectException(f"Your name '{name}' is too long")
    if len(set(name) - set(valid_name_chars)) != 0:
        raise NameIncorrectException(
            f"Your name '{name}' contain incorrect symbols")
    if name[0] in digits:
        raise NameIncorrectException(
            f"Your name '{name}' begins from incorrect symbols")

    if len(pwd) < 8:
        raise PasswordIncorrectException(f"Your password '{pwd}' is short")
    if len(set(pwd) - set(digits)) == len(set(pwd)):
        raise PasswordIncorrectException(
            f"Your password '{pwd}' must contain least one digit")
    if len(set(pwd) - set(valid_pwd_chars)) != 0:
        raise PasswordIncorrectException(
            f"Your password '{pwd}' contain incorrect symbols")
    if len(set(pwd) - set(lower_lets)) == len(set(pwd)):
        raise PasswordIncorrectException(
            f"Your password '{pwd}' must contain least one char in lower \
registry")
    if len(set(pwd) - set(upper_lets)) == len(set(pwd)):
        raise PasswordIncorrectException(
            f"Your password '{pwd}' must contain least one char in UPPER \
registry")


# SET of UI function
def clear_screen():
    """
    Функція очистки екрана
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def get_terminal_size():
    """
    повертається поточна ширина(кільк.символів) вікна термінала
    """
    return shutil.get_terminal_size()[0]


def input_int(msg, attempts=3):
    """
    Функція вводу від користувача цілого числа з обробкою невірного вводу

    Params:
        msg - Запрошення для інформування користувача
        attempts - кількість спроб вводу

    Output:
        Повідомлення про невдалі спроби

    Return:
        int - введене приведене число
        Exception (ValueError) - якщо не вдалося отримати адекватні дані від 
            користувача
    """
    accetable_symbs = tuple(str(i) for i in range(10))
    for attempt in range(attempts):
        try:
            text = input(f"{attempt}. {msg}")
            replaced = "".join(
                (char if char in accetable_symbs else " " for char in text)
                )
            lst = replaced.split()
            if len(lst) == 0:
                raise ValueError(f"You Enter wrong integer number: {text}")
            return int(lst[0])
        except ValueError as ex:
            print("Error.", ex)
            wait_key()
            continue

    raise ValueError(
        f"Error. Sorry your: {attempts} attempts of input are wrong.")


def input_float(msg, attempts=3):
    """
    Функція вводу від користувача дійсного числа з обробкою невірного вводу

    Params:
        msg - Запрошення для інформування користувача
        attempts - кількість спроб вводу

    Output:
        Повідомлення про невдалі спроби

    Return:
        float - введене приведене число
        Exception (ValueError) - якщо не вдалося отримати адекватні дані від 
            користувача
    """
    accetable_symbs = tuple(it_chain((".", "-"), (str(i) for i in range(10))))
    for attempt in range(attempts):
        text = input(f"{attempt + 1}. {msg}")
        replaced = "".join(
            (char if char in accetable_symbs else " " for char in text)
            )
        lst = replaced.split()
        if len(lst) == 0:
            print(f"You Enter wrong float number: {text}")
            continue

        try:
            value = round(float(lst[0]), 2)
            return value
        except ValueError as ex:
            print(f"Error. Your entered number: {lst[0]} is not a float. \
Reason: {ex}")
            continue

    raise ValueError(f"Error. Sorry your: {attempts} attempts of input float \
number are wrong.")
