# csv_operations.py
"""
Об'єкти для маніпуляції із даними CSV
"""
import csv

import urllib3
import certifi


class CsvUrlReader:
    def __init__(self, url_source):
        self.url_orders_csv = url_source
        self.csv_lst_orders = []
        http = urllib3.PoolManager(ca_certs=certifi.where())
        response = http.request('GET', self.url_orders_csv)
        if response.status == 200:
            reader = csv.DictReader(response.data.decode().splitlines())
            for row in reader:
                self.csv_lst_orders.append(row)
        else:
            raise Exception(f"Sorry does not load need orders from: "
                            f"{self.url_orders_csv}. "
                            f"Причина: {response.status}")

    def __iter__(self):
        self.current_idx = 0
        return self

    def __next__(self):
        index_item = self.current_idx
        self.current_idx += 1
        if index_item == len(self.csv_lst_orders):
            raise StopIteration
        return self.csv_lst_orders[index_item]
