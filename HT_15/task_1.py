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


class ScraperSite:
    BASE_URL = "https://www.expireddomains.net/domain-lists/"
    
    def __init__(self):
        self._session = requests.Session()
        self._domains = []
        self._sub_domains = {}

        self.scrape_page(self.BASE_URL)

    @property
    def domains(self) -> list:
        return self._domains

    @property
    def sub_domains(self) -> dict:
        return self._sub_domains

    def get_sub_domains(self, domain) -> list:
        return self._sub_domains[domain]

    def scrape_page(self, url):
        scrapped_data = ScraperTitlePage(self, url).data
        self._domains = scrapped_data[0]
        self._sub_domains = scrapped_data[1]

    # todo - add other functionality

    def close(self):
        self._session.close()

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

    def __init__(self, manager):
        self._session = manager._session
        self._response_content = None
        self._response_content = self.get_response_content(manager.BASE_URL)
        # self._response_encoding = manager.encoding

    @staticmethod
    def url_to_file_name(url: str) -> str:
        f_name = url.replace("://", "__").replace(".", "_").replace("/", "_").strip("_") + ".cache"
        print(f"Modi url to file: {f_name}")
        return f_name

    # @property
    # def encoding(self) -> str:
    #     return self._response_encoding

    def get_response_content(self, url) -> requests.Response.content:
        tmp_file_name = ScraperPageBase.url_to_file_name(url)
        response_content = None
        if exists(tmp_file_name):
            print(f"no Get read cached file: {tmp_file_name}")
            with open(tmp_file_name, "rb") as f:
                response_content = f.read()
        elif not self._response_content:
            print(f"GET to: {url}")
            response = self._session.get(url)
            response_content = response.content
            if not exists(tmp_file_name):
                with open(tmp_file_name, "wb") as f:                                                                                                                                                                                                                                          
                    f.write(response_content)
        else:
            print(f"Sorry problem Get {url} or read cached file {tmp_file_name}")

        return response_content


@dataclass
class SubDomainInfo:
    text: str
    url: str


class ScraperTitlePage(ScraperPageBase):
    def __init__(self, manager: ScraperSite, url: str):
        super().__init__(manager)
        self._response_content = self.get_response_content(url)

    @property
    def data(self) -> (list, dict):
        domains = []
        sub_domains = {}
        if self._response_content:
            page_soup = BeautifulSoup(self._response_content, 'lxml')
            # box_header_soup = page_soup.select(".box-header")
            overviews_soup = page_soup.select(".overview")
            
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

    # @property
    # def present_sub_domain(self) -> list:
    #     lst = []
    #     if self._response_content:
    #         page_soup = BeautifulSoup(self._response_content, 'lxml')
    #         box_header_soup = page_soup.select(".box-header")
    #         for item in box_header_soup:
    #             lst.append(item.text.strip())
    #     return lst


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

    url_to_next = [item.url for item in scrape_site.sub_domains[domain] if item.text == sub_domain][0]
    print(f"{url_to_next=} next relative link")

    scrape_site.close()


# class ExpireddomainsScrappy:
#     BASE_URL = "https://www.expireddomains.net/domain-lists/"

#     def __init__(self):
#         self._session = requests.Session()
#         self._response = get_response(self.BASE_URL)
#         self._response_encoding = None
#         self.AVIALIBLE_DOMAIN_ZONES = self.get_list_present_domain_zones()

#     @staticmethod
#     def url_to_file_name(url: str) -> str:
#         return url.replace("://", "__").replace(".", "_").replace("", "_") + ".html"

#     def get_response(self, url: str) -> requests.Response:
#         tmp_file_name = ExpireddomainsScrappy.url_to_file_name(url)
#         if not self._response:
#             response = self._session.get(url)
#             self._response_encoding = response.encoding
#             if not exsists(tmp_file_name):
#                 with open(tmp_file_name, "w", encoding=self._response_encoding) as f:
                                                                                                                                                                                                                                              
#                     f.write(response)
#         else:
#             if exsists(tmp_file_name):
#                 with open(tmp_file_name, )
#                 response = 
#         return response

#     def get_list_present_domain_zones(self) -> list:
#         lst = []
#         page_soup = BeautifulSoup(self._response, 'lxml')
#         box_header_soup = page_soup.select(".box-header")
#         for item in box_header_soup


