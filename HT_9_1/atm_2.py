# atm_2.py

# # Додаткове завдання HT_9_1

# ## Програма-банкомат. (із застосуванням sqllite)
   
#  ### Використовуючи функції створити програму з наступним функціоналом:
#    - підтримка 3-4 користувачів, які валідуються парою ім'я/пароль (файл <users.json>);
#    - кожен з користувачів має свій поточний баланс (table balance) 
#    - історію транзакцій (teble transactions);
#    - є можливість:
#      - переглянути стан рахунку;
#      - вносити гроші;
#      - знімати гроші
#    - Обов'язкова перевірка введених даних:
#      - введено цифри; 
#      - знімається не більше, ніж є на рахунку
#      - і т.д.
        
#  ###  Особливості реалізації:
#    - таблиця з балансом - оновлюється кожен раз при зміні балансу (містить просто цифру з балансом);
#    - таблиця транзакцій - кожна транзакція у вигляді рядка додається в таблицю;
#    - таблиця з користувачами (якщо ви зайшли адміном): 
#      - додавання нового користувача 
#      - видалення користувача
        
#  ### Особливості функціонала:
#    - за кожен функціонал відповідає окрема функція;
#    - основна функція - <start()> - буде в собі містити весь workflow банкомата:
#    - на початку роботи - логін користувача (програма запитує ім'я/пароль). 
#       Якщо вони неправильні - вивести повідомлення про це і закінчити роботу (хочете - зробіть 3 спроби, а потім вже закінчити роботу - все на ентузіазмі :))
#    - потім - елементарне меню типу:
#    ```
#    Введіть дію:
#      1. Подивитись баланс
#      2. Поповнити баланс
#      3. Зняти кошти
#      0. Вихід
#    ```
#    - далі - фантазія і креатив, можете розширювати функціонал, але основне завдання має бути повністю реалізоване :)

#   P.S. Добре продумайте структуру програми та функцій

import os
import json
import sqlite3
from sqlite3 import Error


users = None

class UserLogonFallied(Exception):
    """
    Виключна ситуація - проблема входу в банкомат
    """
    pass 


def cls():
    """
    Функція очистки екрана
    """
    os.system('cls' if os.name=='nt' else 'clear')


def start():
    """
    Основна ф-ія роботи із ATM
    """
    cls()

    # Prepare
    users = get_start_users("users.json")
    print(f"{users}")
    conn = prepare_db("database.db", users) 
    if not conn:
        # Problemm connect to DB - need exit
        return None

    # login

def prepare_db(db_file_name, def_users):
    """
    Підготовка БД до подальшої роботи (нормалізація)

    повертаємо 
     - об'єкт під'єднання якщо все вдалося
     - None - якщо виникли проблеми
    """
    fl_create_def_users = False
    if not os.path.exists(db_file_name):
        # файл БД не існує - потрібно наповнити БД відповідно до def_users
        fl_create_def_users = True

    # try connect
    conn = None 
    try:
        conn = sqlite3.connect(db_file_name)
    except Error as ex:
        print(f"Sorry problem to connect DB: {db_file_name}, need to quit")
        print(ex)
        return

    # Connect success
    # Create need tables
    sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL
        )
    """
    helper_create_table(conn, sql, "users")

    sql = """
        CREATE TABLE IF NOT EXISTS balance (
            id INTEGER PRIMARY KEY, 
            value DECIMAL(10,2)
        )
    """
    helper_create_table(conn, sql, "balance")

    sql = """
        CREATE TABLE IF NOT EXISTS transaction_ (
            id          INTEGER,
            date_time   TIMESTAMP,
            message     TEXT,
            PRIMARY KEY("id","date_time")        
        )
    """
    helper_create_table(conn, sql, "transaction_")

    # Fill empty bd for testing
    if fl_create_def_users:
        # потрібно наповнити таблиці
        cur = conn.cursor()
        # fill table users
        users = tuple((item, ) for item in def_users)
        print(users)
        cur.executemany("INSERT INTO users (name) VALUES(?)", users)
        conn.commit()
        # fill table balance
        empty_balances = ((row[0], 0.0) for row in cur.execute("SELECT * FROM users").fetchall() if row[1] != "admin")
        cur.executemany("INSERT INTO balance (id, value) VALUES (?, ?)", empty_balances)
        conn.commit()
        # fill transaction not needed

    return conn

def helper_create_table(conn, sql, name_table_msg):
    """
    Допоміжна функція створення потрібної таблиці

    Визиває Exception - якщо проблема
    """
    try:
        cur = conn.execute(sql)
        conn.commit()
    except Error as ex:
        print(f"Sorry problem to create {name_table_msg} table, need to quit")
        print(ex)
        raise 


def get_start_users(file_name):
    """
    Отримати словник користувач:пароль із файла вказаного в file_name

    Якщо файл відсутній - то повертаємо тільки параметри адміна і почнемо із 
    порожньої чи існуючої БД  
    """
    dct = dict()

    if os.path.exists(file_name):
        with open(file_name) as f:
            dct = json.load(f)

    dct["admin"] = "barBarMiaKirGudoo6"
    
    return dct

# def 




# import csv
# import os
# from datetime import datetime

# user_transaction = []




# def start():
#     """
#     Футкція звпуску банкомата
#     """
#     cls()
#     print("Begin work ATM.")

#     if not os.path.exists("users.csv"):
#         raise FileExistsError("Sorry need file users.csv did not found.")

#     av_users = get_users()
#     av_usert_str = ",".join((f"{key}({value})" if key == "alex" else key for key, value in av_users.items()))

#     attemts = 3
#     for attemt in range(attemts):
#         try:
#             print(f"Available users are: {av_usert_str}")
#             user, pwd = input(f"{attemt + 1:>2} of {attemts:>2}. Login user. Enter user and password separated by space: ").split(" ")
#         except ValueError as ex:
#             if attemts - attemt == 1: 
#                 raise UserLogonFallied("Login Fallied. You used all attemts for login. Bye")
#             continue

#         if len(user) > 0 and len(pwd) > 0: 
#             if user in av_users.keys() and av_users[user] == pwd: 
#                 # Succes login
#                 print("Login success. Begin work...")
#                 user_workflow(user)
#                 break
#         print(f"You enter wrong user or password. Try againn. Remained: {attemts - attemt - 1} attempt(s)")

#     print("Work is done")
                



# def user_workflow(user):
#     """
#     Цикл роботи з користувачем після автентифікації
#     """
#     fn_user_balance = f"{user}_balance.txt"
#     fn_transaction = f"{user}_transaction.json"
#     if not os.path.exists(fn_user_balance) or not os.path.exists(fn_transaction):  
#         print("Need user files created.")
#         create_new_users_files(fn_user_balance, fn_transaction)

#     load_transactions(user)

#     user_ch = user_menu(user)


# def user_menu(user):
#     """
#     Вивід меню та отримання від користувача його вибір
#     """
#     lst = [
#         ("1. Look at the balance", look_balance),
#         ("2. Top up the balance", top_up_balance),
#         ("3. Withdraw funds", withdraw_funds),
#         ("x. Exit", done_user_workflow),
#         ]

#     choice = None    
#     log_transaction("Open new session to work with user")
#     while choice != "x":
#         cls()
#         print(f"ATM #1 - for: {user}")
#         print("What do you need?")
#         for item in lst: 
#             print(item[0])

#         choice = input("Made you choice: ")
#         if choice in choiсes_menu(lst):
#             # Call apropriate function
#             lst[index_menu(lst, choice)][1](user)


# def choiсes_menu(lst_menu):
#     """
#     Повертає генератор - ключі символи вибору меню, знач. до .  
#     """
#     return (item[0].split(".")[0] for item in lst_menu)

# def index_menu(lst_menu, choice):
#     """
#     Повертає індекс пункта меню
#     """
#     for idx, item in enumerate(lst_menu):
#         if item[0].split(".")[0] == choice:
#             return idx


# def get_balance(user):
#     """
#     Отримати поточний баланс
#     """
#     with open(f"{user}_balance.txt") as f:
#         value = float(f.read())

#     return value

# def look_balance(user):
#     """
#     Переглянути Баланс користувача
#     """
#     value = get_balance(user)
#     log_transaction(f"Operation Viewing the balance: {value:.2f}")
#     print(f"Your balance: {value:.2f}")
#     _ = input("Press Enter to Continue ...")

# def top_up_balance(user):
#     """
#     Поповнення балансу
#     """
#     try:
#         inp = input("Enter sum (float with 2 decimal) to top up balance: ")
#         value = abs(round(float(inp), 2))
#         modi_balance(user, value)
#         log_transaction(f"Operation top up balance to: {value}")
#     except ValueError as ex:
#         log_transaction(f"Operation top up balance by: {inp}, interrrupted you enetered wrong value.")
#         print(f"Sorry You enter wrong value: {inp}. Try again")
#         _ = input("Press Enter to Continue ...")


# def write_balance(user, value):
#     """
#     Занести у файл значення поточного балансу
#     """
#     with open(f"{user}_balance.txt", "w") as f:
#         f.write(str(value))

# def modi_balance(user, value):
#     """
#     Зміна величини баланса + поповнити - зняття
#     """
#     curr_balance = get_balance(user)
    
#     if value > 0:
#         write_balance(user, round(curr_balance + value, 2))
#     else:
#         if curr_balance < abs(value):
#             print("You don't have enough funds")
#             log_transaction(f"Fail. Operation withdraw funds to: {value}. Current balance: {curr_balance}")
#             _ = input("Press Enter to Continue ...")
#         else:
#             write_balance(user, round(curr_balance - abs(value), 2))   

# def withdraw_funds(user):
#     """
#     Зняття готівки
#     """
#     try:
#         inp = input("Enter sum (float with 2 decimal) to withdraw funds: ")
#         value = abs(round(float(inp), 2))
#         modi_balance(user, -value)
#         log_transaction(f"Operation withdraw_funds by: {value}")
#     except ValueError as ex:
#         log_transaction(f"Operation withdraw_funds by: {inp}, interrrupted you enetered wrong value.")
#         print(f"Sorry. Operation withdraw_funds. You enter wrong value: {inp}. Try again")
#         _ = input("Press Enter to Continue ...")


# def done_user_workflow(user):
#     """
#     Закінчити роботу з банкоматом
#     """
#     print("Close user session ... ")
#     log_transaction(f"End workflow. Close current session.")
#     # dump string for comfortable view log
#     log_transaction(f"#") 

#     save_transactions(user)


# def load_transactions(user):
#     """
#     Завантажити у список поточний переілік транзакцій користувача
#     """
#     lst = None
#     with open(f"{user}_transaction.json") as f:
#         lst = json.load(f)
    
#     user_transaction.extend(lst)

# def save_transactions(user):
#     """
#     Записати у файл користувача перелік його транзакцій, що міститься у 
#     списку транзакцій
#     """
#     with open(f"{user}_transaction.json", "w") as f:
#         json.dump(user_transaction, f, indent=4)

# def log_transaction(msg):
#     """
#     Додати нове повідомлення у список транзакцій
#     """
#     time_stamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
#     user_transaction.append(f"{time_stamp}-{msg}")
    

# def create_new_users_files(fn_user_balance, fn_transaction):
#     """
#     Створюються нові файли для підтримки користувача, за їх повної,
#     або часткової відсутності
#     """
#     with open(fn_user_balance, "w") as f: 
#         f.write("0.0")

#     with open(fn_transaction, "w") as f: 
#         f.write("[]")


if __name__ == "__main__":
    start()