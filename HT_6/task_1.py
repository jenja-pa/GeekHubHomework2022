# task_1.py
# 1. Створіть функцію, всередині якої будуть записано СПИСОК із п'яти 
#  користувачів (ім'я та пароль). 
# Функція повинна приймати три аргументи: 
#  * два - обов'язкових (<username> та <password>) 
#  * третій - необов'язковий параметр <silent> (значення за замовчуванням - <False>).
# Логіка наступна:
    # якщо введено правильну пару ім'я/пароль - вертається True;
    # якщо введено неправильну пару ім'я/пароль:
        # якщо silent == True - функція повертає False
        # якщо silent == False - породжується виключення LoginException (його також треба створити =))

class WrongUserException(Exception):
    pass

def test_credential(username, password, silent=False):
    """
    Функція перевірки імені та пароля

    Вхідні дані: 
        * username - ім'я користувача
        * password - пароль користувача
        * silent   - реакція на неправильно введені ім'я та пароль користувача 

    Вихідні дані: 
     * True чи False 
     * створюємо виключення якщо silent==False і непройдено перевірку

    """
    pwds = [
        ("garry", "roMunel67"),
        ("tom", "gabRT67"),
        ("simon", "34TRObert"),
        ("josh34", "armeNT32tab"),
        ("gabriel", "qwerTY567")
    ]

    if any(map(lambda item: item[0] == username and item[1] == password, pwds)):
        return True
    else:
        if silent:
            return False
        else:
            raise WrongUserException("You pass not not existing username or password.")

if __name__ == "__main__":
    print("1 silent: False")
    usr = input("Enter username: ")
    pwd = input("Enter pasword: ")
    print(f"Result test credential: {test_credential(usr, pwd)}")

    print("2 silent: True")
    usr = input("Enter username: ")
    pwd = input("Enter pasword: ")
    print(f"Result test credential: {test_credential(usr, pwd, True)}")
