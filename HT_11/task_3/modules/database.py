"""
database.py

Модуль операцій по роботі з Базою даних

"""
import traceback
import sqlite3

from sqlite3 import Error
from datetime import datetime

import modules.utilites as utils


class UserLogonFalliedError(Exception):
    """
    Виключна ситуація - проблема входу в банкомат
    Перевіряється по БД
    """


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
        conn.commit()
    except Error as ex:
        print("Error insert into log_atm. Reason:", ex)
        utils.wait_key()


def add_log_transaction(conn, db_user_info, message):
    """
    Ведення логу роботи із банкоматом по користувачу
    """
    print("db.add_log_transaction")
    print(f"{conn}, {db_user_info=}, {message=}")
    utils.wait_key()
    try:
        conn.execute(
            """
            INSERT INTO log_transactions 
            (id_user, id_session, date_time, message)
            VALUES (?, ?, ?, ?)""", 
            (db_user_info["id"], db_user_info["id_session"], datetime.now(), 
                message))
        conn.commit()
    except Error as ex:
        print("Error. Problem insert message to transaction users log.")
        print("Delails are:", ex)
        utils.wait_key()
        add_log_atm(
            conn, 
            f"Error insert log message for user:{db_user_info['name']}, \
session:{db_user_info['id_session']}  to transaction users log")
        add_log_atm(conn, f"Exception message: {ex}")
        add_log_atm(conn, "#")


def get_transaction(conn, db_user_info):
    """
    Видача переліку транзакцій по користувачу
    """
    rows = helper_db_select_rows(
        conn, """SELECT ROWID, id_session, id_user, date_time, message 
FROM log_transactions 
WHERE id_user=?""", 
        "Does not able SELECT from log_transactions", 
        (db_user_info["id"], ))
    return rows


def get_full_transaction(conn):
    """
    Видача переліку усіх транзвкцій
    """
    rows = helper_db_select_rows(
        conn, """
SELECT date_time, message FROM (
    SELECT date_time, message FROM log_atm
    UNION
    SELECT l.date_time, '(' || u.name || '): ' || l.message as message 
    FROM log_transactions l LEFT OUTER JOIN users u on l.id_user = u.id
) ORDER BY date_time
""", "Does not able SELECT from log_* tables")
    
    return rows


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


def helper_db_select_rows(conn, sql, err_msg, args=None):
    """
    Допоміжна функція - повернення
    -переліку рядків за допомогою sql із
        БД вказаної в conn, 

    * err_msg - Повідомлення про помилку
    * args - Можливі аргументи до SQL
    """
    try:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        if args is None:
            cur.execute(sql)
        else:
            cur.execute(sql, args)
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


def set_db_modify_user_balance(conn, db_user_info, value_to_modify_deposit):
    """
    Модифікація балансу користувача
    """
    helper_db_change_data(
        conn, 
        "UPDATE users set balance=?+? WHERE id=?", (
            (db_user_info["balance"], 
                value_to_modify_deposit, db_user_info["id"]),)
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
