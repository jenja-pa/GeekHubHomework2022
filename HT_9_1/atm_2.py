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
import shutil


dct_admin = {"admin": "barBarMiaKirGudoo6"}


class UserLogonFallied(Exception):
    """
    Виключна ситуація - проблема входу в банкомат
    """
    pass 



def start():
    """
    Основна ф-ія роботи із ATM
    """
    cls()

    # Prepare DB
    prepare_db("database.db") 

    # login ATM
    with connect_db("database.db") as conn:
        logon_user = None
        users = get_db_users(conn)
        # print("users:", users)
        avialible_users = ", ".join(user if user != "alex" else f"{user}({pwd})"  for id, user, pwd in users)
        try:
            logon_user = login_user(users, f"Available users are: {avialible_users}")
        except UserLogonFallied as ex:
            print("Sorry. You does not enter correct user login. Bye.", ex)
            return
        else:
            # Get user info from users to further work
            if logon_user in dct_admin.keys():
                # Admin logon
                print("Admin logon")
            else:
                logon_user = next(filter(lambda item: item[1] == logon_user, users))
                print(logon_user)

        # workflow_user()


# SET of UI function
def cls():
    """
    Функція очистки екрана
    """
    os.system('cls' if os.name=='nt' else 'clear')


def align_center_terminal(value, width):
    """
    Функція вирівнювання виводу по центру термінала
    """
    spaces = (width - len(str(value))) // 2
    return " " * spaces + str(value) + " " * spaces


def get_terminal_size():
    """
    повертається поточна ширина(кільк.символів) вікна термінала 
    """
    return shutil.get_terminal_size()[0]


def move_cursor_to_n_lines_up(n):
    """
    Переміщення курсора термінала на n рядків вверх
    """
    print(f"\\033[{n}A")


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
        Exception (ValueError) - якщо не вдалося отримати адекватні дані від користувача
    """
    ACCETABLE_SYMBS = tuple(str(i) for i in range(10))
    for attempt in range(attempts):
        try:
            text = input(f"{attemt}.", msg)
            replaced = "".join((char if char in ACCETABLE_SYMBS else " " for char in text)) 
            lst = replaced.split()
            if len(lst) == 0:
                raise ValueError(f"You Enter wrong integer number: {text}")
            return int(lst[0])
        except ValueError as ex:
            print("Error.", ex)
            _ = input("Press Enter")
            move_cursor_to_n_lines_up(2)
            continue

    raise ValueError(f"Error. Sorry your: {attempts} attempts of input are wrong.")


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
        Exception (ValueError) - якщо не вдалося отримати адекватні дані від користувача
    """
    ACCETABLE_SYMBS = tuple(".", *tuple(str(i) for i in range(10)))
    for attempt in range(attempts):
        try:
            text = input(f"{attemt}.", msg)
            replaced = "".join((char if char in ACCETABLE_SYMBS else " " for char in text)) 
            lst = replaced.split()
            if len(lst) == 0:
                raise ValueError(f"You Enter wrong float number: {text}")
            return float(lst[0])
        except ValueError as ex:
            print("Error.", ex)
            _ = input("Press Enter")
            move_cursor_to_n_lines_up(2)
            continue

    raise ValueError(f"Error. Sorry your: {attempts} attempts of input are wrong.")


def output_lines(seq):
    """
    Вивід на екран термінала рядка чи рядків, вирівненого по центру
    """
    if len(seq) > 0:
        if isinstance(seq, list, tuple):
            for item in seq:
                print(align_center_terminal(str(item)), get_terminal_size())
        else:
            print(align_center_terminal(str(seq)), get_terminal_size())


def input_logon(attempt, msg_input="Login user. Enter user and password separated by space"):
    """
    Спроба ввести користувача та пароль

    Return:
        Якщо введено два значення розділені пробілом - повертаємо їх
        інакше генеруємо виключення ValueError
    """
    text = input(f"{attempt + 1:>2}. {msg_input}: ")
    try:
        user, pwd, *_ = text.split(" ")
    except Exception as ex:
        raise ValueError(f"Not correct input: {text}, need-> user password")
    return user, pwd

def choice_menu(msg="Available users are: ...not passed...", attempts=3):
    """
    Функція формує запит на вхід користувача у банкомат

    Input:
        * items - перелік для формування пунктів меню
            (text, key, fun_to_call)

    Return:
        * Повертає інформацію про вибраний пункт
    """
    pass

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


# Logic workflow
def login_user(db_users, title="Available users are: ...not passed...", attempts=3):
    """
    Проведення спроби входу користувача

    Return:
        Повериаємо name користувача який здійснив вхід, це може бути і адміністратор
    """
    print(title)
    dct_users = {user: pwd for id, user, pwd in db_users}
    for attempt in range(attempts):
        try:
            user, pwd = input_logon(attempt)
            #handler admin 
            if dct_admin.get(user, None) is not None:
                if dct_admin[user] == pwd:
                    print("logon ADMIN Success")
                    return user
            # test user and password
            if dct_users.get(user, None) is None:
                raise UserLogonFallied(f"Sorry. Entered user: {user}, are not avialible")
            if dct_users[user] != pwd:
                raise UserLogonFallied(f"Sorry. Entered password for user: {user} are wrong")
        except ValueError as ex:
            print(ex)
            continue
        except UserLogonFallied as ex:
            print(ex)
            continue
        except Exception as ex:
            print("Unhandled.", ex)
        else:
            # logon succefnll
            print("logon SUCCESS")
            return user
    raise UserLogonFallied("You spent all attempts to logon. Work ended.")


# SET of DB functions
def connect_db(db_file_name):
    """
    Забезпечення приєднання до БД

    Повертаємо об'єкт connection або None при неудачі
    """
    conn = None 
    try:
        conn = sqlite3.connect(db_file_name)
    except Error as ex:
        print(f"Sorry problem to connect DB: {db_file_name}, need to quit")
        print(ex)
    return conn


def prepare_db(db_file_name):
    """
    Створення порібної нам структури БД для подальшої роботи
    та проведення підготовчих дій по снаповненню початковими даними (нормалізація БД)

    input:
        conn - об'єкт з'єднання 
    """
    # Create need tables if one not exsists
    with connect_db(db_file_name) as conn:
        sql = """
            CREATE TABLE IF NOT EXISTS users (
                name TEXT NOT NULL,
                password TEXT NOT NULL,
                PRIMARY KEY("name")        
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

        if len(get_db_users(conn)) == 0: 
            # таблиця користувачів порожня - наповнюємо її із можливо наданого users.json
            # якщо users.json не надано - там буде тільки admin
            
            # remove data in other tables
            helper_DML(conn, "DELETE FROM balance")
            helper_DML(conn, "DELETE FROM transaction_")

            #fill and prepare tables
            json_users = get_json_users("users.json")
            prepare_users = tuple((user, pwd) for user, pwd in json_users.items())
            helper_DML(conn, "INSERT INTO users (name, password) VALUES (?, ?)", prepare_users)

            db_users = get_db_users(conn)
            prepare_balances = tuple((row[0], 0.0) for row in db_users)
            helper_DML(conn, "INSERT INTO balance (id, value) VALUES (?, ?)", prepare_balances)


# getter DB value(s)
def get_db_users(conn):
    """
    Допоміжна функція - отримання списку доступних користувачів із БД
    """
    return helper_select_rows(conn, "SELECT rowid, name, password FROM users", "Trouble select from users")    

# Допоміжні функції отриманна даних із БД
def helper_select_value(conn, sql, err_msg):
    """
    Допоміжна функція - повернення одного значення за допомогою sql із 
        БД вказаної в conn, err_msg - Повідомлення про помилку
    """
    try:
        cur = conn.cursor()
        cur.execute(sql)
        return cur.fetchone()[0]
    except Error as ex:
        print("Error.", err_msg)
        print(ex)
        raise

def helper_select_row(conn, sql, err_msg):
    """
    Допоміжна функція - повернення одного рядка за допомогою sql із 
        БД вказаної в conn, err_msg - Повідомлення про помилку
    """
    try:
        cur = conn.cursor()
        cur.execute(sql)
        return cur.fetchone()
    except Error as ex:
        print("Error.", err_msg)
        print(ex)
        raise

def helper_select_rows(conn, sql, err_msg):
    """
    Допоміжна функція - повернення переліку рядків за допомогою sql із 
        БД вказаної в conn, err_msg - Повідомлення про помилку
    """
    try:
        cur = conn.cursor()
        cur.execute(sql)
        return cur.fetchall()
    except Error as ex:
        print("Error.", err_msg)
        print(ex)
        raise

def helper_DML(conn, sql, args = None):
    """
    Виконання запиту зміни дани
    """
    try:
        cur = conn.cursor()
        if args is None:
            cur.execute(sql)
        elif len(args) == 1:
            cur.execute(sql, args)
        else:
            cur.executemany(sql, args)
        conn.commit()
    except Error as ex:
        if len(args) == 0:
            print(f"Error. Execution {sql}")
        else:
            print(f"Error. Execution {sql} with params: {args}")
        raise

def helper_create_table(conn, sql, name_table_msg):
    """
    Допоміжна функція створення потрібної таблиці

    Визиває Exception - якщо проблема
    """
    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
    except Error as ex:
        print(f"Sorry problem to create {name_table_msg} table, need to quit")
        print(ex)
        raise 


def get_json_users(file_name):
    """
    Отримати словник користувач:пароль із файла вказаного в file_name

    Якщо файл відсутній - то повертаємо тільки параметри адміна і почнемо із 
    порожньої чи існуючої БД  
    """
    dct = dict()

    if os.path.exists(file_name):
        with open(file_name) as f:
            dct = json.load(f)
    
    return dct





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