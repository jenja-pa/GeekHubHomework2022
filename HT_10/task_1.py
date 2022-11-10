"""
task_1.py

# HT #10
## Банкомат 3.0
[X] реалізуйте видачу купюр за логікою видавання найменшої кількості купюр, 
    але в межах наявних в банкоматі. 
      Наприклад: 2560 --> 2х1000, 1х500, 3х20. 
      Будьте обережні з "жадібним алгоритмом"! 
[ ] Видані купюри також мають бути “вилучені” з банкомату. 
  Тобто якщо до операції в банкоматі було 
    5х1000, 5х500, 5х20 - має стати 3х1000, 4х500, 2х20.
[X] як і раніше, поповнення балансу користувача не впливає на кількість купюр
    Їх кількість може змінювати лише інкасатор.

[ ] обов’язкова реалізація таких дій (назви можете використовувати свої):

  Інтерфейс меню:
    При запуску:
       -  Вхід
       -  Реєстрація (з перевіркою валідності/складності введених даних)
       -  Вихід

    Для користувача:
       -  Баланс
       -  Поповнення my: інтерактивне поповнення
       -  Зняття
       -  [ ]Історія транзакцій
       -  Вихід на стартове меню

    Для інкасатора:
       -  Наявні купюри/баланс тощо
       -  Зміна кількості купюр
       -  [ ]Повна історія операцій по банкомату (дії всіх користувачів
        та інкасаторів)
       -  Вихід на стартове меню
  ```
**P.S.**
- [ ] обов’язкове дотримання РЕР8 (якщо самостійно ніяк, 
то https://flake8.pycqa.org/en/latest/ вам в допомогу)
- [ ] (опціонально) не лініться і придумайте якусь свою особливу 
фішку/додатковий функціонал, але при умові що основне завдання виконане
"""

import traceback
import sqlite3

from sqlite3 import Error
from datetime import datetime
from itertools import chain as it_chain, count as it_count

import utils
import database as db
from select_stack_bills import form_stack_bills, create_stack_bills, NotEnoughCostInATMError, NotPossibleSelectSetBanknotesError


def output_lines(value):
    """
    Вивід на екран термінала рядка чи рядків, вирівненого по центру
    """
    if value is None:
        # Nothing to output
        return
    if isinstance(value, str):
        for item in map(lambda line: line.strip(), value.split("\n")):
            if item:
                print(item)
    elif isinstance(value, list, tuple):
        for item in value:
            print(str(item).strip())
    else:
        print(str(value).strip(), 10)


def choice_menu(title, items, footer):
    """
    Функція що показує форму для вибору варыанта дії(меню)

    Input:
        * title - Заголовок
        * items - перелік для формування пунктів меню
            ((text, key, fun_to_call), ...)
        * footer- Закінчення меню

    Return:
        * Повертає кортеж із інформацію про вибраний пункт
    """
    utils.clear_screen()
    output_lines(title)
    lst_keys = []
    for text, key, _ in items:
        lst_keys.append(key)
        output_lines(text)
    output_lines(footer)
    # move_cursor_to_n_lines_up(2)

    while True:
        char = utils.wait_key("Choose your option:")
        if char in lst_keys:
            # acceptable char
            for item in items:
                if item[1] == char:
                    return item


def menu_1_level(conn):
    """
    Формування меню 1го рівня від входу в банкомат
    """
    return choice_menu(f"""## Welcome to ATM v 2.0 sqlite3 powered ##
#-----------------------------------------
#      ATM balance is: {get_db_atm_balance(conn):.2f}
#-----------------------------------------
# key | Description
#-----------------------------------------""", (
        ("#  1. | Create new user", "1", create_new_user),
        ("#  2. | Login to ATM", "2", login_user),
        ("# ", None, None),
        ("#  x. | Exit", "x", exit_atm)
    ), """#-----------------------------------------""")


# SET functions of buissnes logic
def create_new_user(conn):
    """
    Створення нового користувача ATM
    """
    add_log_atm(conn, "Begin create new user ...")
    print()
    print("#-----------------------------------------")
    print("Begin create new user:")
    user_name = input("Enter name for new user: ")
    pwd = input("Enter password for new user: ")
    add_log_atm(conn, f"Testing {user_name=}, password={pwd}")
    try:
        utils.validations_name_password(user_name, pwd)
        set_db_new_user(conn, user_name, pwd)
    except utils.NameIncorrectException as ex:
        add_log_atm(conn, f"Atention your user name '{user_name}' is \
inappropriate. Reason: {ex}")
        print(f"Atention your user name '{user_name}' is inappropriate. \
Reason: {ex}")
    except utils.PasswordIncorrectException as ex:
        add_log_atm(conn, f"Atention your password '{pwd}' is inappropriate. \
Reason: {ex}")
        print(f"Atention your user password '{pwd}' is inappropriate. \
Reason: {ex}")
    except Error as ex:
        add_log_atm(conn, f"Atention this user '{user_name}' cannot be \
applied. Reason: {ex}")
        print(f"Atention this user '{user_name}' cannot be applied. \
Reason: {ex}")
    except Exception as ex:
        add_log_atm(conn, f"Unknown unhandled error. Reason: {ex}")
        print("You are have Unknown error.", ex)
    else:
        add_log_atm(
            conn, 
            f"User {user_name}/{pwd} created successfuly and ready to use")
        print(f"User {user_name}/{pwd} created successfuly and ready to use")

    utils.wait_key()


def exit_atm(conn):
    """
    Функція, що визивається при кінцевому виході із ATM
    """
    add_log_atm(conn, "User ended work with ATM")
    print("Exit from ATM")


def input_logon(
        attempt, 
        msg_input="Enter user and password separated by space"):
    """
    Спроба ввести користувача та пароль

    Return:
        Якщо введено два значення розділені пробілом - повертаємо їх
        інакше генеруємо виключення ValueError
    """
    text = input(f"{attempt + 1:>3}. {msg_input}: ")
    try:
        user, pwd, *_ = text.split(" ")
    except ValueError:
        raise ValueError(f"You input is empty or only user: '{text}', \
            need-> user(space)password.")
    return user, pwd


def login_user(conn, attempts=3):
    """
    Проведення спроби входу користувача

    * Отримуємо пару user/password
    * Перевіряємо user/password на правильність
    * в залежності від типу користувача визиваємо наступне меню
    """
    add_log_atm(conn, "Begin process login to ATM")
    utils.clear_screen()
    dct_users = get_db_users(conn)
    avialible_users = ",".join(
        user if user not in ("admin", "alex") 
        else f"{user}/{dct_users[user]['password']}"
        for user in dct_users
        )
    print(f"""
## Login -=- ATM v 2.0 sqlite3 powered                         ##
#        You have try {attempts:>2} attempts to enter                     ##
-----------------------------------------------------------------
# Present users: {avialible_users}
#----------------------------------------------------------------
""")
    for attempt in range(attempts):
        try:
            user, pwd = input_logon(attempt)
            # test user and password
            if dct_users.get(user, None) is None:
                raise utils.UserLogonFalliedError(
                    f"Sorry. Entered user: {user}, are not avialible")
            if dct_users[user]["password"] != pwd:
                raise utils.UserLogonFalliedError(
                    f"Sorry. Entered password for user: {user} are wrong")

            db_user_info = dct_users[user]
            # user login success
            session_id = \
                get_db_max_session4user_id(conn, db_user_info["id"]) + 1
            db_user_info["id_session"] = session_id

            # handler admin
            if db_user_info["permision"] & 1 == 1:
                print("        logon ADMIN Success")
                add_log_atm(conn, "Begin Administrator session.")
                admin_workflow(conn, db_user_info)
                print("        logout ADMIN")
                add_log_atm(conn, "End Administrator session.")
            else:
                # simple user
                print("        logon USER Success")
                add_log_atm(conn, f"Begin User:{user} session.")
                user_workflow(conn, db_user_info)
                print(f"        logout USER {user}")

            return

        except ValueError as ex:
            print(ex)
            add_log_atm(
                conn, 
                f"attempt: {attempt + 1}. You Fallied to Login. user: {ex}")
            continue
        except db.UserLogonFalliedError as ex:
            print(ex)
            add_log_atm(
                conn, 
                f"attempt: {attempt + 1}. You Fallied to Login. user: {user}")
            continue
        except Exception as ex:
            # traceback.print_exc()
            # print("Unhandled.", ex.line_number, sys.exc_info(), ex)
            add_log_atm(conn, f"attempt: {attempt + 1}. Unknown error {ex}")

    print("You spent all attempts to login. Try again later. Press any key...")
    utils.wait_key()
    add_log_atm(conn, "You spent all attempts to login. Try again later.")


# Функції підтримки роботи адміністратора
def admin_workflow(conn, db_user_info):
    """
    Робочий процес адміністратора
    """
    # В подальшому можливо вставити сюди меню для вибору із
    # більше ніж 1 варіанта дії, зараз дія одна тому просто
    # її запускаємо
    change_cnt_of_banknotes(conn, db_user_info)


def change_cnt_of_banknotes(conn, db_user_info):
    """
    Перегляд модифікація наявності купюр у банкоматі
    """
    # Словник поточного стану наповненості купюрами банкомату
    dct_idx_b_current_state = {
        str(idx): (nominal, cnt) for idx, (nominal, cnt)
        in zip(it_count(1), get_db_banknotes(conn).items())
        }
    while (choice_char := menu_banknotes(conn, dct_idx_b_current_state)) \
            != "x":
        nominal, cur_cnt = dct_idx_b_current_state[choice_char]
        change_banknote_count(conn, db_user_info, nominal, cur_cnt)
        dct_idx_b_current_state = {
            str(idx): (nominal, cnt) for idx, (nominal, cnt)
            in zip(it_count(1), get_db_banknotes(conn).items())
            }


def menu_banknotes(conn, dct_idx_b_current_state):
    """
    Формування меню переліку кількості банкнот у банкоматі
    dct_idx_b_current_state - перелік стану наявних банкнон
    """
    utils.clear_screen()

    print(f"""
## Change Count of banknotes ATM v 2.0 sqlite3                   #
#-----------------------------------------------------------------
# ATM balance is: {get_db_atm_balance(conn):.2f}
#-----------------------------------------------------------------
# key |Nominal| |Count of""")
    for idx, (nominal, cnt) in dct_idx_b_current_state.items():
        print(f"# {idx:>3}. {nominal:>5} = {cnt:>4} ")

    print("""#
#   x. Exit
#-----------------------------------------------------------------
# Press key of your choice to change count of banknotes ...""")
    # Перебор вводу від користувача доки не отримаємо із заявленого переліку
    accetable_chars = tuple(it_chain(dct_idx_b_current_state.keys(), ("x", )))
    while (choice_char := utils.wait_key(None).lower()) not in accetable_chars:
        pass

    return choice_char


def change_banknote_count(conn, db_user_info, nominal, cnt):
    """
    Отримати від користувача потрібну кількість
    банкнот вказаного моміналу
    Занести отриману кулькість в таблицю

    nominal, cnt = який номінал змінювати, поточне значення
    """
    try:
        value = utils.input_int(f"Present {cnt} banknotes for nominal \
\"{nominal}\". Enter new value: ")
        add_log_transaction(
            conn, db_user_info,
            f"User enter: {value} new count of banknotes, nominal:{nominal}")
        set_db_banknote_count(conn, db_user_info, nominal, value)
        add_log_transaction(
            conn, db_user_info,
            f"Value of new count: {value} of banknotes nominal:{nominal}, \
commit in DB")
    except ValueError:
        add_log_transaction(
            conn, db_user_info,
            f"The user could not enter the correct amount of banknotes, \
nominal:{nominal}")


# Функції підтримки роботи простого користувача
def user_workflow(conn, db_user_info):
    """
    Робочий процес простого користувача
    """
    # print("user_workflow")
    # key = utils.wait_key()
    menu_result = ("", "0", None)

    add_log_transaction(
        conn, db_user_info,
        f"User {db_user_info['name']} begin session to work with ATM")
    while menu_result[1] != "x":
        menu_result = menu_user_level(conn, db_user_info)
        if menu_result[2] is not None:
            menu_result[2](conn, db_user_info)
            # поновлення даних по користувачу (save №сесії між поновленнями)
            current_session_id = db_user_info["id_session"]
            db_user_info = get_db_user_info(conn, db_user_info["id"])
            db_user_info["id_session"] = current_session_id

    add_log_transaction(
        conn, db_user_info,
        f"User {db_user_info['name']} ended session to work with ATM")


def menu_user_level(conn, db_user_info):
    """
    Формування меню простого користувача що зайшов у банкомат
    """
    return choice_menu(
            f"""## User menu to ATM v 2.0 sqlite3 powered ################
#---------------------------------------------------------
# ATM balance is: {get_db_atm_balance(conn):.2f}
# Welcome {db_user_info['name']} your balance is: {db_user_info['balance']:.2f}
#---------------------------------------------------------""",
            (
                ("# 1. Deposit to your account", "1", user_deposit_acc),
                ("# 2. Withdraw funds", "2", user_withdraw_funds),
                ("# ", None, None),
                ("# x. Exit", "x", user_exit)
            ), """
#---------------------------------------------------------""")


def user_deposit_acc(conn, db_user_info):
    """
    Поповнення рахунку користувачем
    """
    print("User performs to deposit money:")

    min_nominals = min(item for item in get_db_banknotes(conn).keys())

    try:
        value = utils.input_float(
            "Please enter sum to deposite (float. sample: 125.67): ")
        if value < 0:
            raise ValueError(
                f"Sorry value of funds must be larger zero not {value:.2f}")
    except ValueError as ex:
        print(ex)
        utils.wait_key()
        return

    add_log_transaction(
        conn, db_user_info,
        f"User: {db_user_info['name']} want to deposit {value:.2f}$ ")

    real_value_to_deposit = (value // min_nominals) * min_nominals

    set_db_balance(conn, db_user_info, real_value_to_deposit)
    add_log_transaction(
        conn, db_user_info,
        f"for user: {db_user_info['name']}:{db_user_info['balance']:.2f} \
make accruals {real_value_to_deposit:.2f}$ and change:\
        {round(value - real_value_to_deposit, 2):.2f}")

    print(f"You provided: {value:.2f}$, enrolled: \
        {real_value_to_deposit:.2f}$, change: \
        {round(value - real_value_to_deposit, 2)}$")
    utils.wait_key()


def user_withdraw_funds(conn, db_user_info):
    """
    Зняття коштів користувачем
    """
    print("User performs to withdraw money:")

    try:
        value = utils.input_float(
            "Please enter sum to withdraw (float. sample: 125.67): ")
        if value < 0:
            raise ValueError(
                f"Sorry value of funds must be larger zero not {value:.2f}")
    except ValueError as ex:
        print(ex)
        utils.wait_key()
        return

    # Введену суму вирівняти на 10
    value = int((value // 10) * 10)

    atm_balance = get_db_atm_balance(conn)
    user_balance = db_user_info["balance"]
    add_log_transaction(
        conn, db_user_info,
        f"User: {db_user_info['name']} want to withdraw {value:.2f}$. \
From your account: {user_balance:.2f}$")
    try:
        if value > user_balance:
            add_log_transaction(
                conn, db_user_info,
                f"Refused. Withdraw {value:.2f}$. Overbalance your account: \
{user_balance:.2f}$")
            raise ValueError(f"Sorry. Your balance: {user_balance}$ \
                does not allow withdraw {value}$")
        if value > atm_balance:
            add_log_transaction(
                conn, db_user_info,
                f"Refused. Withdraw {value:.2f}$. Overbalance ATM \
account: {atm_balance:.2f}$")
            raise ValueError(f"Sorry. ATM has: {atm_balance}$ only does \
not allow withdraw {value}$")

        add_log_transaction(
            conn, db_user_info,
            f"Accepted to withdraw. User: {db_user_info['name']} get {value:.2f}$ \
from balance: {user_balance:.2f}$")
        # Провести генераціюб банкнот до видачі
        stack_atm = create_stack_bills(get_db_banknotes(conn))
        try:
            stack_user = form_stack_bills(value, stack_atm) 
            # Зміна баланса користувача
            set_db_balance(conn, db_user_info, -value)
            # Зміна кількості банкнот в ATM та занесення змін у БД
            for nominal in stack_user:
                set_db_banknote_count(
                    conn, db_user_info, nominal, 
                    stack_atm[nominal] - stack_user[nominal])
            print(f"You want to take off {value}. \
Given out banknotes: ", end="")
            lst = [
                f"{cnt}*{nominal}" for nominal, cnt in 
                filter(lambda item: item[1] > 0,  stack_user.items())]
            print(", ".join(lst))
        except NotPossibleSelectSetBanknotesError:
            add_log_transaction(
                conn, db_user_info,
                f"Refused. Withdraw {value:.2f}$ \
to user:{db_user_info['name']}. ATM does not have appropriate banknots to get")
        except Exception:
            print(str(traceback.format_exc()))
        # NotEnoughCostInATMError -ця помилка передб-на але не повинна виникати

        add_log_transaction(
            conn, db_user_info,
            f"User: {db_user_info['name']} new balance: \
{round(user_balance - value, 2):.2f}$")

    except ValueError as ex:
        print("Error.", ex)
    else:
        print("Operation Withdraw_funds - Success")

    utils.wait_key()


def user_exit(conn, db_user_info):
    """
    Визивається при завершенні роботи користувача з банкоматом
    """
    add_log_transaction(
        conn, db_user_info,
        f"The user {db_user_info['name']} wanted to quit. Final balance \
is {db_user_info['balance']}")


# SET of DB functions
def connect_db(db_file_name):
    """
    Забезпеченнdb.я приєднання до БД

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
    та проведення підготовчих дій по снаповненню початковими даними
     (нормалізація БД)

    input:
        db_file_name - шлях до БД
    """
    # Create need tables if one not exsists
    with connect_db(db_file_name) as conn:
        sql = """CREATE TABLE IF NOT EXISTS "users" (
            id    INTEGER NOT NULL UNIQUE,
            name  TEXT NOT NULL UNIQUE,
            password  TEXT NOT NULL,
            balance   DECIMAL(10, 2) NOT NULL,
            permision INTEGER NOT NULL,
            PRIMARY KEY("id" AUTOINCREMENT)
            )"""
        helper_db_change_data(conn, sql)

        sql = """CREATE TABLE IF NOT EXISTS log_transactions (
            ROWID       integer not null UNIQUE,
            id_user     INTEGER not null,
            id_session  INTEGER not null,
            date_time   TIMESTAMP not null,
            message     TEXT,
            PRIMARY KEY(ROWID AUTOINCREMENT)        
            )
        """
        helper_db_change_data(conn, sql)

        sql = """CREATE TABLE IF NOT EXISTS log_atm (
            ROWID       integer not null UNIQUE,
            date_time   TIMESTAMP not null,
            message     TEXT,
            PRIMARY KEY(ROWID AUTOINCREMENT)        
            )"""
        helper_db_change_data(conn, sql)

        # banknotes
        sql = """CREATE TABLE IF NOT EXISTS atm_banknotes (
            nominal INTEGER not null UNIQUE,
            cnt     INTEGER not null,
            PRIMARY KEY(nominal)        
            )
        """
        helper_db_change_data(conn, sql)

        if len(get_db_users(conn)) == 0:
            # таблиця користувачів порожня - тому проводимо наповнюємо БД
            # мінімально потрібними початковими даними

            # remove data in other tables
            helper_db_change_data(conn, "DELETE FROM log_transactions")
            helper_db_change_data(conn, "DELETE FROM log_atm")
            helper_db_change_data(conn, "DELETE FROM atm_banknotes")

            # first fill begins data - Вставляємо адміна
            helper_db_change_data(conn, """
                INSERT INTO users (id, name, password, balance, permision) 
                VALUES (?,?,?,?,?)""", ((1, "admin", "admin", 0.0, 1), ))
            helper_db_change_data(conn, """
                INSERT INTO users (id, name, password, balance, permision) 
                VALUES (?,?,?,?,?)""", ((2, "a", "a", 0.0, 1), ))
            # Наповнюємо класифікатор наявних номіналів банкнот
            avialible_nominals = (10, 20, 50, 100, 200, 500, 1000)
            prepare_banknotes = ((item, 0) for item in avialible_nominals)
            helper_db_change_data(
                conn, 
                "INSERT INTO atm_banknotes (nominal, cnt) VALUES (?, ?)",   
                tuple(prepare_banknotes))


def add_log_atm(conn, message):
    """
    Ведення логу роботи із банкоматом без прив'язки до користувача
    """
    try:
        conn.execute(
            "INSERT INTO log_atm (date_time, message) VALUES (?, ?)",
            (datetime.now(), message))
    except Error as ex:
        print("Error insert into log_atm. Reason:", ex)


def add_log_transaction(conn, db_user_info, message):
    """
    Ведення логу роботи із банкоматом по користувачу
    """
    try:
        conn.execute(
            """
            INSERT INTO log_transactions 
            (id_user, id_session, date_time, message)
            VALUES (?, ?, ?, ?)""", 
            (db_user_info["id"], db_user_info["id_session"], datetime.now(), 
                message))
    except Error as ex:
        print("Error. Problem insert message to transaction users log.")
        print("Delails are:", ex)
        add_log_atm(
            conn, 
            f"Error insert log message for user:{db_user_info['name']}, \
session:{db_user_info['id_session']}  to transaction users log")
        add_log_atm(conn, f"Exception message: {ex}")
        add_log_atm(conn, "#")


# Допоміжні функції отриманна даних із БД
def helper_db_select_value(conn, sql, args=None, err_msg="No message"):
    """
    Допоміжна функція - повернення одного значення за допомогою sql з
        можливими параметрами args(tuple) із БД вказаної в conn,
        err_msg - Повідомлення про помилку
    """
    try:
        cur = conn.cursor()
        if args is None:
            cur.execute(sql)
        else:
            if isinstance(args, tuple):
                cur.execute(sql, args)
            else:
                cur.execute(sql, tuple(args))
        return cur.fetchone()[0]
    except Error as ex:
        print("Error.", err_msg, " Reason:", ex)
        print(ex)
        raise


def helper_db_select_row(conn, sql, err_msg):
    """
    Допоміжна функція - повернення одного рядка за допомогою sql із
        БД вказаної в conn, err_msg - Повідомлення про помилку
    """
    try:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(sql)
        return cur.fetchone()
    except Error as ex:
        print("Error.", err_msg)
        print(ex)
        raise


def helper_db_select_rows(conn, sql, err_msg):
    """
    Допоміжна функція - повернення
    -переліку рядків за допомогою sql із
        БД вказаної в conn, err_msg - Повідомлення про помилку
    """
    try:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(sql)
        return cur.fetchall()
    except Error as ex:
        print("Error.", err_msg)
        print(ex)
        raise


def helper_db_change_data(conn, sql, args=None):
    """
    Виконання запиту зміни даних
        conn - об'єкт з'єднання
        sql  - запит, що виконується
        args - можливі аргументи які підставляються в sql
            None - відсутні аргументи, - виконати без підстановки
            len(args) == 1 - тільки 1 рядок
            інакше надано рядків більше 1го
    Return:
        None - якщо виконалось без помилок
        вивід повідомлення та reraise Exception - якщо виникла проблема
    """
    try:
        cur = conn.cursor()
        if args is None:
            cur.execute(sql)
        elif len(args) == 1:
            cur.execute(sql, args[0])
        else:
            cur.executemany(sql, args)
        conn.commit()
    except Error as ex:
        if args is None or len(args) == 0:
            print(f"Error. Execution {sql}. Reason: {ex}")
        else:
            print(f"Error. Execution {sql} with params: {args}. Reason: {ex}")
        raise


# getter DB value(s)
def get_db_users(conn):
    """
    Отримання списку доступних користувачів із БД
    Return:
        dict of dict: dct["user"]{dct info about user}
    """
    rows = helper_db_select_rows(
        conn, "SELECT id, name, password, balance, permision FROM users", 
        "Trouble select all from users")

    return {row["name"]: dict(zip(row.keys(), row)) for row in rows}


def get_db_user_info(conn, id_user):
    """
    Отримання інформаціх про користувача по його id із БД
    Return:
        dict = {dct info about user}
    """
    rows = get_db_users(conn)
    for row in rows.values():
        if row["id"] == id_user:
            return row
    add_log_atm(conn, "Attempt get user information to missing id:{id_user}")
    raise KeyError(f"Error. user with id:{id_user} Not present in our DB.")


def set_db_balance(conn, db_user_info, real_value_to_deposit):
    """
    Модифікація балансу користувача
    """
    helper_db_change_data(
        conn, 
        "UPDATE users set balance=?+? WHERE id=?",
        ((db_user_info["balance"], real_value_to_deposit, db_user_info["id"]),)
        )


def get_db_banknotes(conn):
    """
    Отримання переліку банкнот та їх кількості
    Return:
        dict:  dct["<nominal>"] = cnt
    """
    rows = helper_db_select_rows(
        conn,
        "SELECT nominal, cnt FROM atm_banknotes ORDER BY nominal",
        "Trouble select all from atm_banknotes")
    return {row["nominal"]: row["cnt"] for row in rows}


def set_db_banknote_count(conn, user_info, nominal, value):
    """
    Поновити значення кількості банкнот вкзаного nominal
    """
    try:
        helper_db_change_data(
            conn,
            "UPDATE atm_banknotes SET cnt=? WHERE nominal=?",
            ((value, nominal), ))
    except Error as ex:
        add_log_transaction(
            conn, user_info,
            f"Appear SQL problem to UPDATE count of atm banknote. Reason:{ex}")
        add_log_transaction(conn, user_info, str(traceback.format_exc()))
    except Exception as ex:
        add_log_transaction(
            conn, user_info,
            F"Appear problem to UPDATE count of atm banknote. Reason:{ex}")
        add_log_transaction(conn, user_info, str(traceback.format_exc()))
    else:
        add_log_transaction(
            conn, user_info,
            f"Change count of banknotes {nominal} to {value} performed \
successfuly")


def set_db_new_user(conn, nick, pwd):
    """
    Вставка нового користувача в БД
    """
    cnt = helper_db_select_value(
        conn,
        "SELECT count(*) FROM users WHERE name=?", (nick, ), 
        f"Select count of: {nick}")
    if cnt > 0:
        # user name already present
        raise Error(f"Sorry this user: {nick} already present")

    # id_user = get_db_max_id_users(conn) + 1

    try:
        helper_db_change_data(
            conn,
            """INSERT INTO users (name, password, balance, permision) 
            VALUES(?,?, 0.0, 0)""",
            ((nick, pwd), ))
    except Error as ex:
        add_log_atm(conn, "Exception insert new user. Reason: " + ex)
        print("Exception insert new user. Reason: " + ex)
        utils.wait_key()


def get_db_atm_balance(conn):
    """
    Обчислення балансу банкомата
    """
    return float(helper_db_select_value(
        conn,
        "SELECT sum(nominal * cnt) as balance FROM atm_banknotes"))


def get_db_max_session4user_id(conn, user_id):
    """
    Отримати максимальний існуючий id_session для id_user в log_transactions
    """
    result = helper_db_select_value(
        conn,
        "SELECT max(id_session) FROM log_transactions WHERE id_user=?",
        (user_id, ),
        "Trouble select max(id_session) from log_transactions for \
user_id:{user_id}")
    return 0 if result is None else result


CNT_OF_ATTEMPTS = 3


def start():
    """
    Основна ф-ія роботи із ATM
    """
    utils.clear_screen()

    # Prepare DB
    prepare_db("database.db")

    # first menu
    with connect_db("database.db") as conn:
        conn.row_factory = sqlite3.Row
        menu_result = ("", "0", None)
        while menu_result[1] != "x":
            menu_result = menu_1_level(conn)
            if menu_result[2] is not None:
                menu_result[2](conn)


if __name__ == "__main__":
    start()
