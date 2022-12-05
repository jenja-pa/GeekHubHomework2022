# task_1.py
# https://www.expireddomains.net/godaddy-makeoffer-domains/
# Викорисовуючи requests/BeautifulSoup, заходите на ось цей сайт 
# "https://www.expireddomains.net/domain-lists/"
# (з ним будьте обережні :wink::skull_and_crossbones:), 
# вибираєте будь-яку на ваш вибір доменну зону і парсите список доменів з усіма
# відповідними колонками - доменів там буде десятки тисяч 
# (звичайно ураховуючи пагінацію). 
# Всі отримані значення зберегти в CSV файл.

# UserViewer %KDt4uLZE%L3.ct  

import os
import requests
from bs4 import BeautifulSoup
import csv
import json
import time
from os.path import exists
from os import listdir, remove 
from rich.prompt import Prompt, Confirm
from dataclasses import dataclass
from urllib.parse import urljoin
from requests_throttler import BaseThrottler


class ScraperSite:
    BASE_URL = "https://www.expireddomains.net/"
    BEGIN_URL = "domain-lists/"
    FILE_CSV = "task_1_result.csv"
    FILE_PROXY_PARAM = "my_own_proxy_parameters.json"
    FILE_HEADERS_PARAM = "my_fake_headers_parameters.txt"
      
    def __init__(self):
        self._session = requests.Session()
        self._session.proxies = self.proxies
        self._bt = BaseThrottler(name='base-throttler', delay=1.75)
        self._domains = []
        self._sub_domains = {}
        self._browser_headers = self.fake_headers

        self._bt.start()
        self.scrape_title_page(urljoin(self.BASE_URL, self.BEGIN_URL))
        if exists(self.FILE_CSV):
            os.remove(self.FILE_CSV)

    @property
    def domains(self) -> list:
        return self._domains

    @property
    def sub_domains(self) -> dict:
        return self._sub_domains

    @property
    def session(self) -> requests.Session:
        return self._session

    @property
    def bt(self) -> BaseThrottler:
        return self._bt
 
    def get_sub_domains(self, domain) -> list:
        return self._sub_domains[domain]

    def scrape_title_page(self, url):
        scrapped_data = ScraperTitlePage(self, url).data
        self._domains = scrapped_data[0]
        self._sub_domains = scrapped_data[1]

    @property
    def proxies(self):
        with open(self.FILE_PROXY_PARAM) as f:
            proxies = json.load(f)
        return proxies

    @property
    def fake_headers(self):
        with open(self.FILE_HEADERS_PARAM) as f:
            str_headers = f.read().strip()

        return {
            item.split(":")[0].strip(): item.split(":")[1].strip() 
            for item in str_headers.split("\n")
            }

    def close(self):
        self._session.close()
        self._bt.shutdown()

    def clear_cache(self):
        for item in listdir():
            if item.endswith(".cache"):
                remove(item)
 
    def write_csv(self, headers, data) -> None:
        if not exists(self.FILE_CSV):
            with open(self.FILE_CSV, "w") as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()

        with open(self.FILE_CSV, "a") as file:
            writer = csv.DictWriter(
                file, fieldnames=headers, 
                delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            for row in data:
                dict_row = {
                    name: int(value) if value.isdigit() else value 
                    for name, value in zip(headers, row)}
                writer.writerow(dict_row)

    def __repr__(self):
        return f"""
            ScraperSite(www.expireddomains.net/domain-lists) 
            self.domains:{",".join(self.domains)} - this is 
            list available domains for future work
            
            do not foget to .close() at end of the work
            if work for scrapping site is ended. 
            Use .clear_cache() to clear temporary downloaded files
            """


class ScraperPageBase:

    def __init__(self, manager: ScraperSite, url_relative: str):
        self._manager = manager
        self._page_soup = self.get_page_in_soup(
            urljoin(manager.BASE_URL, url_relative))

    @staticmethod
    def url_to_file_name(url: str) -> str:
        return (url             
                .replace("://", "__").replace(".", "_")
                .replace("/", "_").replace("?", "_").strip("_") + ".cache"
                )

    @property
    def manager(self) -> ScraperSite:
        return self._manager
    
    @property
    def page_soup(self) -> BeautifulSoup:
        return self._page_soup

    def get_page_in_soup(self, url_full) -> None:
        tmp_file_name = ScraperPageBase.url_to_file_name(url_full)
        if exists(tmp_file_name):
            print(f"witout Get read cached file: {tmp_file_name}")
            with open(tmp_file_name, "rb") as f:
                response_content = f.read()
                page_soup = BeautifulSoup(response_content, 'lxml')

        else:
            print(f"GET to: {url_full}")
            response = self.manager.session.get(
                url=url_full, 
                headers=self.manager._browser_headers, verify=False)

            if response.ok: 
                page_soup = BeautifulSoup(response.content, 'lxml')
            else:
                raise (
                    f"GET to: {url_full} is not completed. "
                    f"Reason: {response.status_code}")

            if not exists(tmp_file_name):
                with open(tmp_file_name, "wb") as f:                                                                                                                                                                                                                                          
                    f.write(response.content)

        return page_soup


@dataclass
class SubDomainInfo:
    text: str
    url: str


class ScraperTitlePage(ScraperPageBase):
    def __init__(self, manager: ScraperSite, url_relative: str):
        super().__init__(manager, url_relative)

    @property
    def data(self) -> (list, dict):
        domains = []
        sub_domains = {}
        if self.page_soup:
            overviews_soup = self.page_soup.select(".overview")
            
            for overview_soup in overviews_soup:
                header_soup = overview_soup.select_one(".box-header")
                domain = header_soup.text.strip()
                domains.append(domain)
                lst = []
                css_query = ".box-content ul li a"
                for domain_sub_soup in overview_soup.select(css_query):
                    # print(f"{domain_sub_soup=}")
                    lst.append(SubDomainInfo(
                        text=domain_sub_soup.text.strip(),
                        url=domain_sub_soup["href"]))
                sub_domains[domain] = lst
        return (domains, sub_domains)


class ScraperTablePage(ScraperPageBase):
    def __init__(self, manager: ScraperSite, url_relative: str):
        super().__init__(manager, url_relative)
    
    @property
    def data(self) -> list:
        """ Дані отримані із сторінки """
        # todo - Створити піготовку даних отриманих із сторінки
        lst_result = []
        if self.page_soup:
            lst_trs_soup = self.page_soup.select("table.base1 tbody tr")
            for tr_soup in lst_trs_soup:
                lst_row = []
                for td_soup in tr_soup.select("td"):
                    lst_row.append(td_soup.text.strip())
                lst_result.append(lst_row)
            return lst_result
        return None

    @property
    def headers(self) -> list:
        """ Заголовки даних отриманих із сторінки """
        lst_result = []
        if self.page_soup:
            lst_a = self.page_soup.select("table.base1 thead tr th a")
            lst_result = [item.text for item in lst_a]
            return lst_result
        return None

    @property
    def next_url(self) -> str:
        """Посилання на наступну сторінку 
        або None якщо сторінка остання"""
        if self.page_soup:
            a_next_soup = self.page_soup.select_one(".next")
            if a_next_soup is not None:
                result = a_next_soup["href"]
                return result
        return None


if __name__ == "__main__":
    scrape_site = ScraperSite()
    print(f"{scrape_site=}")
    try:
        domain = Prompt.ask(
            "Enter domain that do you need from given list:", 
            choices=scrape_site.domains, default="GoDaddy")
        sub_domains = scrape_site.get_sub_domains(domain)

        choices = [item.text for item in sub_domains]
        sub_domain = Prompt.ask(
            "Enter sub domain from given list:", 
            choices=choices, 
            default=choices[0])

        next_url_relative = [
            item.url for item in scrape_site.sub_domains[domain] 
            if item.text == sub_domain
            ][0]
        print(f"{next_url_relative=} next relative link")

        # Begin process scrape data
        cnt = 0
        data = None
        header = None
        while True:
            scrape_page_table = ScraperTablePage(
                scrape_site, next_url_relative)

            cnt += 1
            print(
                f"scrape_page_table {cnt} next_url_rel: "
                f"{scrape_page_table.next_url}")

            data = scrape_page_table.data
            if header is None:
                headers = scrape_page_table.headers
            
            scrape_site.write_csv(headers, data)

            if scrape_page_table.next_url is None:
                # todo - need delete last cached file
                cache_fn = ScraperPageBase.url_to_file_name(
                    urljoin(scrape_site.BASE_URL, next_url_relative))
                print(f"Remove last cached file: {cache_fn}")
                try:
                    os.remove(cache_fn)
                except OSError as ex:
                    print(f"Problem to remove: {cache_fn} {ex}")
                    raise

                print("You have reached the maximum page limit.")
                break
            next_url_relative = scrape_page_table.next_url

        print(f"Scrape task ended. Processed {cnt} pages.")
        print("="*35)
        print(f"Result placed in {scrape_site.FILE_CSV}.")
        print()
    finally:
        scrape_site.close()

    time.sleep(0.5)
    print()
    if Confirm.ask("Do You want to clear cache?", default=False):
        scrape_site.clear_cache()
