# - data_operations.py з класами CsvOperations та DataBaseOperations. 
#   * CsvOperations містить метод для читання даних. 
# Метод для читання приймає аргументом шлях до csv файлу де в колонкі ID 
# записані як валідні, так і не валідні id товарів з сайту. 
#   * DataBaseOperations містить метод для запису даних в sqlite3 базу 
# і відповідно приймає дані для запису. 
# Всі інші методи, що потрібні для роботи мають бути приватні/захищені.
import csv
import sqlite3
from os.path import exists

class CsvOperations:
    INPUT_CSV_FILE = "input.csv"

    def __init__(self):
        self._lst_ids = []

    def load(self, input_csv_file_name: None):
        input_csv_file_name = input_csv_file_name | self.INPUT_CSV_FILE
        if exists(input_csv_file_name):
            with open(input_csv_file_name) as file:
                dct_reader = csv.DictReader(file)
                for row in dct_reader:
                    self._lst_ids.append(row["ID"])
        else:
            print("Not present input csv file. Nothing to work.")
        return self._lst_ids


class DataBaseOperations:
    FILE_DB = "databes.db"
    def __init__(self):
        self._conn = None
        if not exists(self.FILE_DB):
            # Create table
            conn = sqlite3.connect(self.FILE_DB)

        conn = sqlite3.connect(db_path)

    
