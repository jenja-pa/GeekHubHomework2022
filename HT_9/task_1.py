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
import json
import sqlite3
from sqlite3 import Error
import shutil

class UserLogonFallied(Exception):
    """
    Виключна ситуація - проблема входу в банкомат
    """
    pass 

# SET of UI function
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


# SET functions of buissnes logic
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
        db_file_name - шлях до БД 
    """
    # Create need tables if one not exsists
    with connect_db(db_file_name) as conn:
        sql = """
            CREATE TABLE IF NOT EXISTS users (
                name TEXT NOT NULL,
                password TEXT NOT NULL,
                balance DECIMAL(10,2) not null,
                permision INTEGER not null,
                PRIMARY KEY("name")        
            )
        """
        helper_create_table(conn, sql, "users")

        sql = """
            CREATE TABLE IF NOT EXISTS log_transactions (
                id_user     INTEGER not null,
                session		INTEGER not null,
                date_time   TIMESTAMP,
                message     TEXT,
                PRIMARY KEY("id_user","session", "date_time")        
            )
        """
        helper_create_table(conn, sql, "log_transaction")

        # banknotes
        sql = """
            CREATE TABLE IF NOT EXISTS atm_banknotes (
                nominal_value	INTEGER primary key not null,
                cnt				INTEGER not null
            )
        """
        helper_create_table(conn, sql, "atm_banknotes")
 
        if len(get_db_users(conn)) == 0: 
            # таблиця користувачів порожня - наповнюємо БД 
            # мінімально початковими даними
            
            # remove data in other tables
            helper_DML(conn, "DELETE FROM log_transactions")
            helper_DML(conn, "DELETE FROM atm_banknotes")

            #first fill begins data
            helper_DML(conn, 
            	"INSERT INTO users (name, password, balance, permision) VALUES (?,?,?,?)", 
            	(("admin", "admin", 0.0, 1), )
            )

            prepare_banknotes = ((item, 0) for item in (10, 20, 50, 100, 200, 500, 1000))
            helper_DML(conn, "INSERT INTO atm_banknotes (nominal_value, cnt) VALUES (?, ?)", 
            	tuple(prepare_banknotes))


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
    Виконання запиту зміни даних
        conn - об'єкт з'єднання
        sql  - запит, що виконується
        args - можливі аргументи які підставляються в sql
            None - відсутні аргументи, - виконати без підстановки
            len(args) == 1 - тільки 1 рядок
            інакше надано рядків більше 1го 
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
        conn.execute(sql)
        conn.commit()
    except Error as ex:
        print(f"Sorry problem to create {name_table_msg} table, need to quit")
        print(ex)
        raise 



def start():
    """
    Основна ф-ія роботи із ATM
    """
    cls()

    # Prepare DB
    prepare_db("database.db") 

    # first menu 
    
    # login ATM


if __name__ == "__main__":
    start()