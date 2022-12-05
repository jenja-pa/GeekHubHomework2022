# - data_operations.py з класами CsvOperations та DataBaseOperations. 
#   * CsvOperations містить метод для читання даних. 
# Метод для читання приймає аргументом шлях до csv файлу де в колонкі ID 
# записані як валідні, так і не валідні id товарів з сайту. 
#   * DataBaseOperations містить метод для запису даних в sqlite3 базу 
# і відповідно приймає дані для запису. 
# Всі інші методи, що потрібні для роботи мають бути приватні/захищені.
import csv
import sqlite3
from sqlite3 import Error
from os.path import exists
from dataclasses import astuple

from rozetka_api import Data as RozetkaData


class CsvOperations:
    INPUT_CSV_FILE = "input.csv"

    def __init__(self):
        self._lst_ids = []

    def load(self, input_csv_file_name=None):
        if input_csv_file_name is None:
            input_csv_file_name = self.INPUT_CSV_FILE

        if exists(input_csv_file_name):
            with open(input_csv_file_name) as file:
                dct_reader = csv.DictReader(file)
                for row in dct_reader:
                    self._lst_ids.append(row["ID"])
        else:
            print("Not present input csv file. Nothing to work.")
        return self._lst_ids


class DataBaseOperations:
    FILE_DB = "database.db"

    def __init__(self):
        self._conn = sqlite3.connect(self.FILE_DB)
        sql = """
        CREATE TABLE IF NOT EXISTS goods (
            id integer PRIMARY KEY,
            title text NOT NULL,
            old_price real NOT NULL,
            current_price real NOT NULL,
            href text NOT NULL,
            brand text NOT NULL,
            category text NOT NULL
            )""".strip()

        try:
            self._conn.execute(sql)
        except Error as ex:
            print("Error CREATE table: goods", ex)

    def insert(self, data_row: RozetkaData):
        sql_delete = "DELETE FROM goods WHERE id=?".strip()
        try:
            self._conn.execute(sql_delete, (data_row.item_id, ))
            self._conn.commit()
        except Error as ex:
            print("Error DELETE operation.", ex)
            raise

        sql = """
        INSERT INTO goods
        (id, title, old_price, current_price, href, brand, category) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        try:
            self._conn.execute(sql, astuple(data_row))
            self._conn.commit()
        except Error as ex:
            print("Error INSERT operation", ex)
            raise

    def close(self):
        self._conn.close()
