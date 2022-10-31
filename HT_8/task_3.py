# task_3.py
# Програма-банкомат.№1
# 
# 3. Програма-банкомат.
#    Використовуючи функції створити програму з наступним функціоналом:
#       - підтримка 3-4 користувачів, які валідуються парою ім'я/пароль (файл <users.CSV>);
#       - кожен з користувачів має свій поточний баланс 
#   (файл <{username}_balance.TXT>) та історію транзакцій (файл <{username_transactions.JSON>);
#       - є можливість як вносити гроші, так і знімати їх. 
#   Обов'язкова перевірка введених даних (введено цифри; 
# знімається не більше, ніж є на рахунку і т.д.).
#    Особливості реалізації:
#       - файл з балансом - оновлюється кожен раз при зміні балансу (містить просто цифру з балансом);
#       - файл - транзакціями - кожна транзакція у вигляді JSON рядка додається в кінець файла;
#       - файл з користувачами: тільки читається. 
# Але якщо захочете реалізувати функціонал додавання нового користувача - не стримуйте себе :)
#    Особливості функціонала:
#       - за кожен функціонал відповідає окрема функція;
#       - основна функція - <start()> - буде в собі містити весь workflow банкомата:
#       - на початку роботи - логін користувача (програма запитує ім'я/пароль). 
# Якщо вони неправильні - вивести повідомлення про це і закінчити роботу 
# (хочете - зробіть 3 спроби, а потім вже закінчити роботу - все на ентузіазмі :))
#       - потім - елементарне меню типн:
#         Введіть дію:
#            1. Подивитись баланс
#            2. Поповнити баланс
#            3. Вихід
#       - далі - фантазія і креатив, можете розширювати функціонал, але основне завдання має 
# бути повністю реалізоване :)
#     P.S. Увага! Файли мають бути саме вказаних форматів (csv, txt, json відповідно)
#     P.S.S. Добре продумайте структуру програми та функцій

import csv
import json
import os
from datetime import datetime

user_transaction = []


class UserLogonFallied(Exception):
    pass 


def cls():
    """
    Функція очистки екрана
    """
    os.system('cls' if os.name=='nt' else 'clear')


def start():
    """
    Футкція звпуску банкомата
    """
    cls()
    print("Begin work ATM.")

    if not os.path.exists("users.csv"):
        raise FileExistsError("Sorry need file users.csv did not found.")

    av_users = get_users()
    av_usert_str = ",".join((f"{key}({value})" if key == "alex" else key for key, value in av_users.items()))

    attemts = 3
    for attemt in range(attemts):
        try:
            print(f"Available users are: {av_usert_str}")
            user, pwd = input(f"{attemt + 1:>2} of {attemts:>2}. Login user. Enter user and password separated by space: ").split(" ")
        except ValueError as ex:
            if attemts - attemt == 1: 
                raise UserLogonFallied("Login Fallied. You used all attemts for login. Bye")
            continue

        if len(user) > 0 and len(pwd) > 0: 
            if user in av_users.keys() and av_users[user] == pwd: 
                # Succes login
                print("Login success. Begin work...")
                user_workflow(user)
                break
        print(f"You enter wrong user or password. Try againn. Remained: {attemts - attemt - 1} attempt(s)")

    print("Work is done")
                

def get_users():
    """
    Отримати словник користувач:пароль із відповідного файла
    """
    dct = dict()
    with open("users.csv") as f:
        reader = csv.DictReader(f)
        for record in reader:
            dct[record["User"]] = record["Password"]
    return dct


def user_workflow(user):
    """
    Цикл роботи з користувачем після автентифікації
    """
    fn_user_balance = f"{user}_balance.txt"
    fn_transaction = f"{user}_transaction.json"
    if not os.path.exists(fn_user_balance) or not os.path.exists(fn_transaction):  
        print("Need user files created.")
        create_new_users_files(fn_user_balance, fn_transaction)

    load_transactions(user)

    user_ch = user_menu(user)


def user_menu(user):
    """
    Вивід меню та отримання від користувача його вибір
    """
    lst = [
        ("1. Look at the balance", look_balance),
        ("2. Top up the balance", top_up_balance),
        ("3. Withdraw funds", withdraw_funds),
        ("x. Exit", done_user_workflow),
        ]

    choice = None    
    log_transaction("Open new session to work with user")
    while choice != "x":
        cls()
        print(f"ATM #1 - for: {user}")
        print("What do you need?")
        for item in lst: 
            print(item[0])

        choice = input("Made you choice: ")
        if choice in choiсes_menu(lst):
            # Call apropriate function
            lst[index_menu(lst, choice)][1](user)


def choiсes_menu(lst_menu):
    """
    Повертає генератор - ключі символи вибору меню, знач. до .  
    """
    return (item[0].split(".")[0] for item in lst_menu)

def index_menu(lst_menu, choice):
    """
    Повертає індекс пункта меню
    """
    for idx, item in enumerate(lst_menu):
        if item[0].split(".")[0] == choice:
            return idx


def get_balance(user):
    """
    Отримати поточний баланс
    """
    with open(f"{user}_balance.txt") as f:
        value = float(f.read())

    return value

def look_balance(user):
    """
    Переглянути Баланс користувача
    """
    value = get_balance(user)
    log_transaction(f"Operation Viewing the balance: {value:.2f}")
    print(f"Your balance: {value:.2f}")
    _ = input("Press Enter to Continue ...")

def top_up_balance(user):
    """
    Поповнення балансу
    """
    try:
        inp = input("Enter sum (float with 2 decimal) to top up balance: ")
        value = abs(round(float(inp), 2))
        modi_balance(user, value)
        log_transaction(f"Operation top up balance to: {value}")
    except ValueError as ex:
        log_transaction(f"Operation top up balance by: {inp}, interrrupted you enetered wrong value.")
        print(f"Sorry You enter wrong value: {inp}. Try again")
        _ = input("Press Enter to Continue ...")


def write_balance(user, value):
    """
    Занести у файл значення поточного балансу
    """
    with open(f"{user}_balance.txt", "w") as f:
        f.write(str(value))

def modi_balance(user, value):
    """
    Зміна величини баланса + поповнити - зняття
    """
    curr_balance = get_balance(user)
    
    if value > 0:
        write_balance(user, round(curr_balance + value, 2))
    else:
        if curr_balance < abs(value):
            print("You don't have enough funds")
            log_transaction(f"Fail. Operation withdraw funds to: {value}. Current balance: {curr_balance}")
            _ = input("Press Enter to Continue ...")
        else:
            write_balance(user, round(curr_balance - abs(value), 2))   

def withdraw_funds(user):
    """
    Зняття готівки
    """
    try:
        inp = input("Enter sum (float with 2 decimal) to withdraw funds: ")
        value = abs(round(float(inp), 2))
        modi_balance(user, -value)
        log_transaction(f"Operation withdraw_funds by: {value}")
    except ValueError as ex:
        log_transaction(f"Operation withdraw_funds by: {inp}, interrrupted you enetered wrong value.")
        print(f"Sorry. Operation withdraw_funds. You enter wrong value: {inp}. Try again")
        _ = input("Press Enter to Continue ...")


def done_user_workflow(user):
    """
    Закінчити роботу з банкоматом
    """
    print("Close user session ... ")
    log_transaction(f"End workflow. Close current session.")
    # dump string for comfortable view log
    log_transaction(f"#") 

    save_transactions(user)


def load_transactions(user):
    """
    Завантажити у список поточний переілік транзакцій користувача
    """
    lst = None
    with open(f"{user}_transaction.json") as f:
        lst = json.load(f)
    
    user_transaction.extend(lst)

def save_transactions(user):
    """
    Записати у файл користувача перелік його транзакцій, що міститься у 
    списку транзакцій
    """
    with open(f"{user}_transaction.json", "w") as f:
        json.dump(user_transaction, f, indent=4)

def log_transaction(msg):
    """
    Додати нове повідомлення у список транзакцій
    """
    time_stamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    user_transaction.append(f"{time_stamp}-{msg}")
    

def create_new_users_files(fn_user_balance, fn_transaction):
    """
    Створюються нові файли для підтримки користувача, за їх повної,
    або часткової відсутності
    """
    with open(fn_user_balance, "w") as f: 
        f.write("0.0")

    with open(fn_transaction, "w") as f: 
        f.write("[]")



if __name__ == "__main__":
    start()