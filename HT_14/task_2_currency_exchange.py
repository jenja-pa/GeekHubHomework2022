# task_2_currency_exchange.py
# import csv
from dataclasses import dataclass
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


@dataclass
class Currency:
    int_code: int
    char_code: str
    cnt: int
    description: str
    value: float


class CurrencyExchangeUAnbuScrapper:
    BASE_URL = 'https://bank.gov.ua/'
    HOME_URL = urljoin(BASE_URL, 'ua/markets/exchangerates')

    def get_site_currency_exchange_list(self, str_date=None) -> [dict]:
        print(
            f"Get: {self.HOME_URL} "
            f"{'' if str_date is None else 'for: ' + str_date}")
        response = requests.get(
            self.HOME_URL, {"date": str_date, "period": "daily"})
        if not response.ok:
            print(f"Error request, code:{response.status_code}")
            return

        page = response.content
        # print("Parse content")
        page_soup = BeautifulSoup(page, 'lxml')

        date_txt = page_soup.select_one("span#exchangeDate").text
        result = self.get_currency_exchanges(
            page_soup.select_one("table#exchangeRates"), 
            date_txt)

        return result

    def get_currency_exchanges(
            self, table_soup: BeautifulSoup, 
            date_txt: str
            ) -> [dict]:
        # header
        header = []
        header_soup = table_soup.select("thead tr th")
        for item in header_soup:
            header.append(item.text.split("\n")[0])
        # print(f"Process parse header done {header=}")

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
                value=float(td_soup_list[4].text.replace(",", "."))
                )
            data.append(row)

        return dict(
            date_txt=date_txt,
            header=header,
            data=data
            )


if __name__ == "__main__":
    scrapper = CurrencyExchangeUAnbuScrapper()
    result = scrapper.get_site_currency_exchange_list()
    print(result)
