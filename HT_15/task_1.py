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

import requests
from bs4 import BeautifulSoup
from os.path import exists
from os import listdir, remove 
from rich.prompt import Prompt
from dataclasses import dataclass #, fields, astuple
from urllib.parse import urljoin
from requests_throttler import BaseThrottler


class ScraperSite:
    BASE_URL = "https://www.expireddomains.net/"
    BEGIN_URL = "domain-lists/"
    
    def __init__(self):
        self._session = requests.Session()
        self._bt = BaseThrottler(name='base-throttler', delay=1.5)
        self._domains = []
        self._sub_domains = {}

        self._bt.start()
        self.scrape_title_page(urljoin(self.BASE_URL, self.BEGIN_URL))

    @property
    def domains(self) -> list:
        return self._domains

    @property
    def sub_domains(self) -> dict:
        return self._sub_domains

    @property
    def session(self):
        return self._session

    def get_sub_domains(self, domain) -> list:
        return self._sub_domains[domain]

    def scrape_title_page(self, url):
        scrapped_data = ScraperTitlePage(self, url).data
        self._domains = scrapped_data[0]
        self._sub_domains = scrapped_data[1]

    # todo - add other functionality

    def close(self):
        self._session.close()
        self._bt.shutdown()

    def clear_cache(self):
        for item in listdir():
            if item.endswith(".cache"):
                remove(item)

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
        # self._response_content = None
        self._page_soup = self.get_page_in_soup(urljoin(manager.BASE_URL, url_relative))

        # self.get_response_content(manager.BASE_URL)
        # self._response_encoding = manager.encoding

    @staticmethod
    def url_to_file_name(url: str) -> str:
        f_name = url.replace("://", "__").replace(".", "_").replace("/", "_").replace("?","_").strip("_") + ".cache"
        # todo - Delete after debuging
        print("-" * 25)
        print(f"Get url: {url}")
        print(f"Modi url to file: {f_name}")
        print("-" * 25)
        return f_name

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
            response = self.manager.session.get(url_full)
            # todo - Місце де можливо кусками читати відповідь, щоб це було не дуже швидко
            page_soup = BeautifulSoup(response.content, 'lxml')

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
                for domain_sub_soup in overview_soup.select(".box-content ul li a"):
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
            result = self.page_soup.select_one(".next")["href"]
            print(f"next_url: {result}")
            return result
        return None


if __name__ == "__main__":
    scrape_site = ScraperSite()
    print(f"{scrape_site=}")
    # print(f"{scrape_site.domains=}")
    # print(f"{scrape_site.sub_domains=}")

    domain = Prompt.ask("Enter domain that do you need:", choices=scrape_site.domains, default="GoDaddy")
    sub_domains = scrape_site.get_sub_domains(domain)
    # print(f"{sub_domains=}")

    choices = [item.text for item in sub_domains]
    sub_domain = Prompt.ask("Enter sub domain:", choices=choices, default=choices[0])

    next_url_relative = [item.url for item in scrape_site.sub_domains[domain] if item.text == sub_domain][0]
    print(f"{next_url_relative=} next relative link")

    # Begin process scrape data
    cnt = 0
    data = None
    header = None
    while True:
        scrape_page_table = ScraperTablePage(scrape_site, next_url_relative)
        # receive data from page
        cnt += 1
        print(f"scrape_page_table {cnt} next_url_rel: {scrape_page_table.next_url}")
        print(f"headers: {scrape_page_table.headers}")

        print(f"data[0]: {scrape_page_table.data[0]}")
        # data = scrape_page_table.data
        # if header is None:
        #     header = scrape_page_table.header
        # next_url = scrape_page_table.next_url
        # cnt += 1
        
        # todo write data to csv
        # ....

        next_url_relative = scrape_page_table.next_url
        if next_url_relative is None:
            break
        input("Press <Enter> to next...")
        break

    print(f"Scrape task ended. Processed {cnt} pages.")
    scrape_site.close()
