# currency_exchange.py
"""
Модуль що буде отримувати курси валют на поточну дату
для використання у банкоматі

можливо буде створено декілька функцій на випадок якщо вз основного 
джерела отримати дані не вдасться, для керування буде створено диспетчер
"""
import csv
import json
# from dataclasses import dataclass, fields, astuple
from dataclasses import dataclass
from urllib.parse import urljoin
from datetime import datetime as dt

import requests
from bs4 import BeautifulSoup


@dataclass
class Currency:
    int_code: int
    char_code: str
    cnt: int
    description: str
    value: float
    value_sale: float


@dataclass
class CurrencyName:
    int_code: int
    char_code: str
    description: str


class CurrencyExchangePbScrapper:
    BASE_URL = 'https://api.privatbank.ua/'
    HOME_URL = urljoin(BASE_URL, 'p24api/exchange_rates') 
    CSV_DICT = "currency_name.csv"
    # ?json&date=01.12.2008

    def __init__(self, p_csv_dict=None):
        self._dict_currency_name = {}
        
        f_name_dict = self.CSV_DICT
        if p_csv_dict is not None:
            f_name_dict = p_csv_dict

        with open(f_name_dict, encoding="utf-8") as f:
            csv_dict_reader = csv.DictReader(f, delimiter=";")
            for row in csv_dict_reader:
                self._dict_currency_name[row["char_code"]] = CurrencyName(
                    int_code=row["int_code"],
                    char_code=row["char_code"],
                    description=row["description"]
                    )

    def currency_exchange_list(self, str_date: str = None):
        if str_date is None:
            str_date = dt.now().strftime("%d.%m.%Y")
        print(f"Get: {self.HOME_URL} date={str_date}")
        response = requests.get(
            self.HOME_URL, 
            params={"json": "", "date": str_date})
        # print(f"{dir(response)=}")
        if not response.ok:
            print(f"Error request, code:{response.status_code}")
            return
        # print(f"{response.content=}")
        json_data = json.loads(response.content.decode('utf8'))
        # print(f"{json_data=}")
        # print(json_data["exchangeRate"][0])

        header = [
            "Числ.Код", 
            "Симв.код", 
            "Кільк.", 
            f"{'Назва':^40}", 
            "Скупка грн.", 
            "Продаж грн."]

        # transform to common view
        data = []
        # print(f"{self._dict_currency_name=}")
        for item in json_data["exchangeRate"]:
            if item["currency"] not in self._dict_currency_name.keys():
                print(f"Attention your 'currency_name.csv' not include "
                      f"information about currency {item['currency']}")
                continue
            data.append(Currency(
                int_code=int(
                    self._dict_currency_name[item["currency"]].int_code),
                char_code=item["currency"],
                cnt=1,
                description=self._dict_currency_name[
                    item["currency"]].description,
                value=float(item["purchaseRateNB"]),
                value_sale=float(item["saleRateNB"])
                ))

        return dict(
            date_txt=str_date,
            header=header,
            data=data
            )


class TodayCurrencyExchangeUAnbuScrapper:
    BASE_URL = 'https://bank.gov.ua/'
    HOME_URL = urljoin(BASE_URL, 'ua/markets/exchangerates')

    def get_site_currency_exchange_list(self) -> [dict]:
        print(f"Get: {self.HOME_URL}")
        response = requests.get(self.HOME_URL)
        if not response.ok:
            print(f"Error request, code:{response.code}")
            return

        page = response.content
        # print("Parse content")
        page_soup = BeautifulSoup(page, 'lxml')

        date_txt = page_soup.select_one("span#exchangeDate").text
        result = self.get_currency_exchanges(
            page_soup.select_one("table#exchangeRates"), date_txt)

        return result

    def get_currency_exchanges(self, table_soup: BeautifulSoup, date_txt):
        # header
        header = []
        header_soup = table_soup.select("thead tr th")
        for item in header_soup:
            header.append(item.text.split("\n")[0])

        # data
        data = []
        data_soup_tr = table_soup.select("tbody tr")
        for row_soup in data_soup_tr:
            td_soup_list = row_soup.select("td") 
            row = Currency(
                int_code=int(td_soup_list[0].select_one(".value").text),
                char_code=td_soup_list[1].text,
                cnt=int(td_soup_list[2].text),
                description=td_soup_list[3].text.strip(),
                value=float(td_soup_list[4].text.replace(",", ".")),
                value_sale=None
                )
            data.append(row)

        return dict(
            date_txt=date_txt,
            header=header,
            data=data
            )


if __name__ == "__main__":
    # scrapper = TodayCurrencyExchangeUAnbuScrapper()
    # result = scrapper.get_site_currency_exchange_list()
    # print(result)

    scrapper = CurrencyExchangePbScrapper("../currency_name.csv")
    # print(scrapper._dict_currency_name)
    data = scrapper.currency_exchange_list(str_date="30.11.2022")
    print(data)
