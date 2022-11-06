# task_1.py
# # HT 9
# ## Банкомат 2.0
#   - усі дані зберігаються тільки в sqlite3 базі даних у відповідних таблицях. 
#     Більше ніяких файлів. 
#     Якщо в попередньому завданні ви добре продумали структуру програми то у
#      вас не виникне проблем швидко адаптувати її до нових вимог.
#   - на старті додати можливість залогінитися або створити нового користувача
#    (при створенні нового користувача, перевіряється відповідність логіну і 
#    	паролю мінімальним вимогам. 
#    	Для перевірки створіть окремі функції)
#   - в таблиці з користувачами також має бути створений унікальний 
#   	користувач-інкасатор, який матиме розширені можливості (домовимось, 
#   	що логін/пароль будуть admin/admin щоб нам було простіше перевіряти)
#   - банкомат має власний баланс
#   - кількість купюр в банкоматі обмежена (тобто має зберігатися номінал та кількість). 
#   	Номінали купюр - 10, 20, 50, 100, 200, 500, 1000
#   - змінювати вручну кількість купюр або подивитися їх залишок в банкоматі 
#   	може лише інкасатор
#   - користувач через банкомат може покласти на рахунок лише суму кратну 
#   	мінімальному номіналу що підтримує банкомат. 
#   	В іншому випадку - повернути "здачу" (наприклад при поклажі 1005 --> 
#   		повернути 5). 
#   	Але це не має впливати на баланс/кількість купюр банкомату, лише збільшується
#   		баланс користувача (моделюємо наявність двох незалежних касет в банкоматі - 
#   		одна на прийом, інша на видачу)
#   - зняти можна лише в межах власного балансу, але не більше ніж є всього в банкоматі.
#   - при неможливості виконання якоїсь операції - вивести повідомлення з причиною:
#   	  * невірний логін/пароль, 
#   	  * недостатньо коштів на рахунку, 
#   	  * неможливо видати суму наявними купюрами тощо.
#   - файл бази даних з усіма створеними таблицями і даними також додайте в репозиторій, 
#   	що б ми могли його використати
import os
import sys
import traceback
import json
import sqlite3
from sqlite3 import Error
import shutil
from datetime import datetime
from itertools import chain as it_chain, count as it_count

class UserLogonFalliedError(Exception):
    """
    Виключна ситуація - проблема входу в банкомат
    """
    pass 


# Thirdh side class for implementation cross platform analogue getch() - function
# ################################
def wait_key():
    ''' Wait for a key press on the console and return it. '''
    result = None
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
# #################################


# =================================
# Раніше розроблена ф-ія перевіркм імені та пароля
class NameIncorrectException(Exception):
    pass

class PasswordIncorrectException(Exception):
    pass

def validations_name_password(name, pwd):
    """
    Перевірка валідності пари:
     * name     - Ім'я
     * pwd      - Пароль 

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
    elif len(name) > 50:
        raise NameIncorrectException(f"Your name '{name}' is too long")
    elif len(set(name) - set(valid_name_chars)) != 0:
        raise NameIncorrectException(f"Your name '{name}' contain incorrect symbols")
    elif name[0] in digits:
        raise NameIncorrectException(f"Your name '{name}' begins from incorrect symbols")

    if len(pwd) < 8:
        raise PasswordIncorrectException(f"Your password '{pwd}' is short")
    elif len(set(pwd) - set(digits)) == len(set(pwd)):
        raise PasswordIncorrectException(f"Your password '{pwd}' must contain least one digit")
    elif len(set(pwd) - set(valid_pwd_chars)) != 0:
        raise PasswordIncorrectException(f"Your password '{pwd}' contain incorrect symbols")
    elif len(set(pwd) - set(lower_lets)) == len(set(pwd)):
        raise PasswordIncorrectException(f"Your password '{pwd}' must contain least one char in lower registry")
    elif len(set(pwd) - set(upper_lets)) == len(set(pwd)):
        raise PasswordIncorrectException(f"Your password '{pwd}' must contain least one char in UPPER registry")
# =================================

# SET of UI function
def cls():
    """
    Функція очистки екрана
    """
    os.system('cls' if os.name=='nt' else 'clear')


def align_from_left(value, width):
    """
    Функція вирівнювання виводу зліва
    """
    return " " * width + str(value)


def get_terminal_size():
    """
    повертається поточна ширина(кільк.символів) вікна термінала 
    """
    return shutil.get_terminal_size()[0]


def move_cursor_to_n_lines_up(n):
    """
    Переміщення курсора термінала на n рядків вверх
    """
    # print(f"\\033[{n}A")
    sys.stdout.write(f"\\033[{n}A")


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
            text = input(f"{attempt}. {msg}")
            replaced = "".join((char if char in ACCETABLE_SYMBS else " " for char in text)) 
            lst = replaced.split()
            if len(lst) == 0:
                raise ValueError(f"You Enter wrong integer number: {text}")
            return int(lst[0])
        except ValueError as ex:
            print("Error.", ex)
            print("Press any key ...")
            wait_key() 
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


def output_lines(value):
    """
    Вивід на екран термінала рядка чи рядків, вирівненого по центру
    """
    if value is None:
        # Nothing to output
        return
    elif isinstance(value, str):
        for item in map(lambda line: line.strip(), value.split("\n")):
            if item:
                print(align_from_left(item, 10))
    elif isinstance(value, list, tuple):
        for item in value:
            print(align_from_left(str(item).strip(), 10))
    else:
        print(align_from_left(str(value).strip(), 10))


def input_logon(attempt, msg_input="Enter user and password separated by space"):
    """
    Спроба ввести користувача та пароль

    Return:
        Якщо введено два значення розділені пробілом - повертаємо їх
        інакше генеруємо виключення ValueError
    """
    text = input(f"       {attempt + 1:>2}. {msg_input}: ")
    try:
        user, pwd, *_ = text.split(" ")
    except Exception as ex:
        raise ValueError(f"        Not correct input: {text}, need-> user password")
    return user, pwd

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
    cls()
    output_lines(title)
    lst_keys = []
    for text, key, _ in items:
        lst_keys.append(key)
        output_lines(text)
    output_lines(footer)
    # move_cursor_to_n_lines_up(2)

    while True:
        char = wait_key()
        if char in lst_keys:
            # acceptable char
            for item in items:
                if item[1] == char:
                    return item

def menu_1_level(conn):
    """
    Формування меню 1го рівня від входу в банкомат
    """
    return choice_menu(
            f"""## Welcome to ATM v 2.0 sqlite3 powered ##########################
#--------------------------------------------------------------------
# ATM balance is: {get_db_atm_balance(conn):.2f}
#--------------------------------------------------------------------""", (
                ("# 1. Create new user", "1", create_new_user),
                ("# 2. Login to ATM", "2", login_user),
                ("# ", None, None),
                ("# x. Exit", "x", exit_atm)
            ), """
#-------------------------------------------------------------------
 Choose one of case ?""")

# SET functions of buissnes logic
def create_new_user(conn):
    """
    Створення нового користувача ATM
    """
    add_log_atm(conn, "Begin create new user ...")
    user_name = input("Enter name for new user: ")
    pwd = input("Enter password for new user: ")
    add_log_atm(conn, f"Testing {user_name=}, password={pwd}")
    try:
        validations_name_password(user_name, pwd)
        set_db_new_user(conn, user_name, pwd)
    except NameIncorrectException as ex:
        add_log_atm(conn, f"Atention your user name '{user_name}' is inappropriate. Reason: {ex}")
        print(f"Atention your user name '{user_name}' is inappropriate. Reason: {ex}")
    except PasswordIncorrectException as ex:
        add_log_atm(conn, f"Atention your password '{pwd}' is inappropriate. Reason: {ex}")
        print(f"Atention your user password '{pwd}' is inappropriate. Reason: {ex}")
    except Error as ex:
        add_log_atm(conn, f"Atention this user '{user_name}' cannot be applied. Reason: {ex}")
        print(f"Atention this user '{user_name}' cannot be applied. Reason: {ex}")
    except Exception as ex:
        add_log_atm(conn, f"Unknown unhandled error. Reason: {ex}")
        print("You are have Unknown error.", ex)
    else:
        add_log_atm(conn, f"User {user_name}/{pwd} created successfuly and ready to use")
        print(f"User {user_name}/{pwd} created successfuly and ready to use")

    input("Press Enter")
 

def exit_atm(conn):
    """
    Функція, що визивається при кінцевому виході із ATM
    """
    add_log_atm(conn, "User ended work with ATM")
    print("        Exit from ATM")

def login_user(conn, attempts=3):
    """
    Проведення спроби входу користувача

    * Отримуємо пару user/password
    * Перевіряємо user/password на правильність
    * в залежності від типу користувача визиваємо наступне меню
    """
    add_log_atm(conn, "Begin process login to ATM")
    cls()
    dct_users = get_db_users(conn)
    avialible_users = ",".join(
        user if user not in ("admin", "alex") else f"{user}/{dct_users[user]['password']}" 
        for user in dct_users
        )
    print(f"""
        ## Login -=- ATM v 2.0 sqlite3 powered ##########################
        ##  You have {attempts} attempts to enter the ATM
        #################################################################
        # Avialible_users: {avialible_users}
        #----------------------------------------------------------------
        # """)
    for attempt in range(attempts):
        try:
            user, pwd = input_logon(attempt)
            # test user and password
            if dct_users.get(user, None) is None:
                raise UserLogonFalliedError(f"        Sorry. Entered user: {user}, are not avialible")
            if dct_users[user]["password"] != pwd:
                raise UserLogonFalliedError(f"        Sorry. Entered password for user: {user} are wrong")

            db_user_info = dct_users[user]    
            # user login success
            # define N session to user
            print("test", get_db_max_session4user_id(conn, db_user_info["id"])) 
            session_id = get_db_max_session4user_id(conn, db_user_info["id"]) + 1
            # append N session to db_user_info
            db_user_info["id_session"] = session_id

            #handler admin 
            if db_user_info["permision"] & 1 == 1:
                print("        logon ADMIN Success")
                add_log_atm(conn, "Begin Administrator session.")
                admin_workflow(conn, db_user_info)
                print("        logout ADMIN")
                add_log_atm(conn, "End Administrator session.")
                return
            else:
                # simple user
                print("        logon USER Success")
                add_log_atm(conn, f"Begin User:{user} session.")
                user_workflow(conn, db_user_info)
                print(f"        logout USER {user}")
                return

        except ValueError as ex:
            print(ex)
            add_log_atm(conn, f"attempt: {attempt + 1}. You Fallied to Login. user: {ex}")
            continue
        except UserLogonFalliedError as ex:
            print(ex)
            add_log_atm(conn, f"attempt: {attempt + 1}. You Fallied to Login. user: {user}")
            continue
        except Exception as ex:
            traceback.print_exc()
            # print("Unhandled.", ex.line_number, sys.exc_info(), ex)
            add_log_atm(conn, f"attempt: {attempt + 1}. Unknown error {ex}")
    
    print("        You spent all attempts to login. Try again later. Press any key...")
    wait_key()
    add_log_atm(conn, "You spent all attempts to login. Try again later.")

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
    dct_idx_b_current_state = {
        str(idx): (nominal, cnt) for idx, (nominal, cnt) in zip(it_count(1), get_db_banknotes(conn).items())
        }
    while (choice_char := menu_banknotes(conn, db_user_info, dct_idx_b_current_state)) != "x":
        nominal, cur_cnt = dct_idx_b_current_state[choice_char]
        modi_banknote(conn, db_user_info, nominal, cur_cnt)
        dct_idx_b_current_state = {
            str(idx): (nominal, cnt) for idx, (nominal, cnt) in zip(it_count(1), get_db_banknotes(conn).items())
            }


def menu_banknotes(conn, db_user_info, dct_idx_b_current_state):
    """
    Формування меню переліку кількості банкнот у банкоматі
    dct_idx_b_current_state - перелік стану наявних банкнон
    """
    cls()

    print(f"""
## Change Count of banknotes ATM v 2.0 sqlite3                   #
#-----------------------------------------------------------------
# ATM balance is: {get_db_atm_balance(conn):.2f}
#-----------------------------------------------------------------""")
    for idx, (nominal, cnt) in dct_idx_b_current_state.items():
        print(f"# {idx:>3}. {nominal:>5} = {cnt:>4} ")

    print("""#
#   x. Exit
#-----------------------------------------------------------------
 Choose one of them to edit: """)
    # Перебор вводу від користувача доки не отримаємо із заявленого переліку
    while (choice_char := wait_key().lower()) not in it_chain(dct_idx_b_current_state.keys(), ("x", )):
        pass

    return choice_char 

def modi_banknote(conn, db_user_info, nominal, cnt):
    """
    Отримати від користувача потрібну кількість 
    банкнот вказаного моміналу
    Занести отриману кулькість в таблицю

    nominal, cnt = який номінал змінювати, поточне значення
    """
    try:
        value = input_int(f"Present {cnt} banknotes for nominal \"{nominal}\". Enter new value: ")
        set_db_banknote_cnt(conn, db_user_info, nominal, value)
    except ValueError:
        pass


def user_workflow(conn, db_user_info):
    """
    Робочий процес простого користувача
    """
    print("user_workflow")
    key = wait_key()



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
        db_file_name - шлях до БД 
    """
    # Create need tables if one not exsists
    with connect_db(db_file_name) as conn:
        sql = """
            CREATE TABLE IF NOT EXISTS users (
                id          INTEGER not null,
                name        TEXT NOT NULL,
                password    TEXT NOT NULL,
                balance     DECIMAL(10,2) not null,
                permision   INTEGER not null,
                PRIMARY KEY("name")        
            )
        """
        helper_DML(conn, sql)

        sql = """
            CREATE TABLE IF NOT EXISTS log_transactions (
                id_user     INTEGER not null,
                id_session  INTEGER not null,
                date_time   TIMESTAMP not null,
                message     TEXT,
                PRIMARY KEY("id_user","id_session", "date_time")        
            )
        """
        helper_DML(conn, sql)

        sql = """
            CREATE TABLE IF NOT EXISTS log_atm (
                ID          integer primary key not null,
                date_time   TIMESTAMP not null,
                message     TEXT
            )
        """
        helper_DML(conn, sql)

        # banknotes
        sql = """
            CREATE TABLE IF NOT EXISTS atm_banknotes (
                nominal	INTEGER primary key not null,
                cnt		INTEGER not null
            )
        """
        helper_DML(conn, sql)
 
        print(get_db_users(conn))
        if len(get_db_users(conn)) == 0: 
            # таблиця користувачів порожня - тому проводимо наповнюємо БД 
            # мінімально потрібними початковими даними
            
            # remove data in other tables
            helper_DML(conn, "DELETE FROM log_transactions")
            helper_DML(conn, "DELETE FROM atm_banknotes")

            #first fill begins data - Вставляємо адміна
            helper_DML(conn, 
            	"INSERT INTO users (id, name, password, balance, permision) VALUES (?,?,?,?,?)", 
            	((1, "admin", "admin", 0.0, 1), )
            )
            helper_DML(conn, 
                "INSERT INTO users (id, name, password, balance, permision) VALUES (?,?,?,?,?)", 
                ((2, "a", "a", 0.0, 1), )
            )
            # Наповнюємо класифікатор наявних номіналів банкнот
            prepare_banknotes = ((item, 0) for item in (10, 20, 50, 100, 200, 500, 1000))
            helper_DML(conn, "INSERT INTO atm_banknotes (nominal, cnt) VALUES (?, ?)", 
            	tuple(prepare_banknotes))


def add_log_atm(conn, message):
    """
    Ведення логу роботи із банкоматом без прив'язки до користувача
    """
    try:
        conn.execute("INSERT INTO log_atm (date_time, message) VALUES (?, ?)", (datetime.now(), message))
    except Error as ex:
        print("Error insert into log_atm. Details are:")

def add_log_transaction(conn, db_user_info, message):
    """
    Ведення логу роботи із банкоматом по користувачу
    """
    try:
        conn.execute(
            """INSERT INTO log_transactions (id_user, id_session, date_time, message) 
            VALUES (?, ?, ?, ?)""", (db_user_info["id"], db_user_info["id_session"], datetime.now(), message)
            )
    except Error as ex:
        print("Error. Problem insert message to transaction users log. Delails are:")
        print(ex)
        add_log_atm(conn, f"Error insert log message for user:{db_user_info['name']}, session:{db_user_info['id_session']}  to transaction users log")
        add_log_atm(conn, f"Exception message: {ex}")
        add_log_atm(conn, f"#")


# Допоміжні функції отриманна даних із БД
def helper_select_value(conn, sql, args=None, err_msg="No message"):
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

def helper_select_row(conn, sql, err_msg):
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

def helper_select_rows(conn, sql, err_msg):
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

def helper_DML(conn, sql, args = None):
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
            print(f"Error. Execution {sql}")
        else:
            print(f"Error. Execution {sql} with params: {args}")
        raise 

# getter DB value(s)
def get_db_users(conn):
    """
    Отримання списку доступних користувачів із БД
    Return:
        dict of dict: dct["user"]{dct info about user}
    """
    rows = helper_select_rows(conn, 
        "SELECT id, name, password, balance, permision FROM users", 
        "Trouble select all from users"
        )
    return {row["name"]: {key: value for key, value in zip(row.keys(), row)} for row in rows}

def get_db_banknotes(conn):
    """
    Отримання переліку банкнот та їх кількості
    Return:
        dict:  dct["<nominal>"] = cnt
    """
    rows = helper_select_rows(conn, 
        "SELECT nominal, cnt FROM atm_banknotes ORDER BY nominal", 
        "Trouble select all from atm_banknotes"
        )
    return {row["nominal"]: row["cnt"] for row in rows}

def set_db_banknote_cnt(conn, user_info, nominal, value):
    """
    Поновити значення кількості банкнот вкзаного nominal
    """
    try:
        helper_DML(conn, "UPDATE atm_banknotes SET cnt=? WHERE nominal=?", ((value, nominal), ))
    except Error as ex:
        add_log_transaction(conn, user_info, "Appear SQL problem to UPDATE count of atm banknote")        
        add_log_transaction(conn, user_info, str(traceback.format_exc()))        
    except Exception as ex:
        add_log_transaction(conn, user_info, "Appear problem to UPDATE count of atm banknote")
        add_log_transaction(conn, user_info, str(traceback.format_exc()))        
    else:
        add_log_transaction(conn, user_info, f"Change count of banknotes {nominal} to {value} performed successfuly")


def set_db_new_user(conn, nick, pwd):
    """
    Вставка нового користувача в БД
    """
    cnt = helper_select_value(conn, "SELECT count(*) FROM users WHERE name=?", (nick, ), f"Select count of: {nick}")
    if cnt > 0:
        # user name already present
        raise Error(f"Sorry this user: {nick} already present")

    id_user = get_db_max_id_users(conn) + 1
    
    try:
        helper_DML(conn, 
            "INSERT INTO users (id, name, password, balance, permision) VALUES(?,?,?, 0.0, 0)",
            ((id_user, nick, pwd), )
            )
    except Exception as ex:
        add_log_atm(conn, "Exception insert new user. Reason: " + ex)
        print("Exception insert new user. Reason: " + ex)
        input("Press enter after reading...")
    

def get_db_atm_balance(conn):
    """
    Обчислення балансу банкомата
    """
    return float(helper_select_value(conn, "SELECT sum(nominal * cnt) as balance FROM atm_banknotes"))

def get_db_max_id_users(conn):
    """
    Отримати максимальний існуючий id
    """
    return helper_select_value(conn, "SELECT max(id) FROM users", err_msg="Trouble select max(id) from users")

def get_db_max_session4user_id(conn, user_id):
    """
    Отримати максимальний існуючий id_session для id_user в log_transactions
    """
    result = helper_select_value(conn, 
        "SELECT max(id_session) FROM log_transactions WHERE id_user=?", 
        (user_id, ),
        "Trouble select max(id_session) from log_transactions for user_id:{user_id}"
        )
    return 0 if result is None else result 



CNT_OF_ATTEMPTS = 3

def start():
    """
    Основна ф-ія роботи із ATM
    """
    cls()

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