# task_3.py
# Програма-банкомат.№1
#  Не буду опмсувати умови щоб не засмічувати код

import csv
import json
import os


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
    print("Begin work ATM.")

    if not os.path.exists("users.csv"):
        raise FileExistsError("Sorry need file users.csv did not found.")

    av_users = get_users()

    attemts = 3
    for attemt in range(attemts):
        try:
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
    while choice != "x":
        cls()
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


def look_balance(user):
    """
    Переглянути Баланс користувача
    """
    value = get_balance(user)
    print(f"Your balance: {value:.2f}")
    _ = input("Press Enter: ")


def top_up_balance(user):
    """
    Поповнити баланс
    """
    try:
        inp = input("Enter sum (float with 2 decimal) to top up balance: ")
        value = abs(round(float(inp), 2))
    except ValueError as ex:
        print(f"Sorry You enter wrong value: {inp}. Try again")

    modi_balance(user, value)


def get_balance(user):
    """
    Отримати поточний баланс
    """
    with open(f"{user}_balance.txt") as f:
        value = float(f.read())

    return value

def write_balance(user, value):
    """
    Занести значення поточного балансу
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
            _ = input("Press Enter")
        else:
            write_balance(user, round(curr_balance - abs(value), 2))   


def withdraw_funds(user):
    """
    Зняти готівку
    """
    try:
        inp = input("Enter sum (float with 2 decimal) to withdraw funds: ")
        value = abs(round(float(inp), 2))
    except ValueError as ex:
        print(f"Sorry You enter wrong value: {inp}. Try again")

    modi_balance(user, -value)


def done_user_workflow(user):
    """
    Закінчити роботу з банкоматом
    """
    print("Close user session ... ")


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