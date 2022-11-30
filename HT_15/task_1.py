# task_1.py
# https://www.expireddomains.net/godaddy-makeoffer-domains/
# Викорисовуючи requests/BeautifulSoup, заходите на ось цей сайт 
# "https://www.expireddomains.net/domain-lists/"
# (з ним будьте обережні :wink::skull_and_crossbones:), 
# вибираєте будь-яку на ваш вибір доменну зону і парсите список доменів з усіма
# відповідними колонками - доменів там буде десятки тисяч 
# (звичайно ураховуючи пагінацію). 
# Всі отримані значення зберегти в CSV файл.

import requests
from bs4 import BeautifulSoup
from os.path import exists
from os import os_listdir, os_remove 

class ScraperSite:
    BASE_URL = "https://www.expireddomains.net/domain-lists/"
    
    def __init__(self):
        self._session = requests.Session()
        self.domains = self.BASE_URL
        # self._encoding = None

    @property
    def domains(self) -> list:
        return self._domains

    @domains.setter
    def domains(self, url):
        self._domains = ScraperTitlePage(self, url).present_domain_zones
    
    # todo - add other functionality

    def close(self):
        self._session.close()

    def clear_cache(self):
        for item in os_listdir():
            if item.endswith(".cache"):
                os_remove(item)

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


class ScraperTitlePage(ScraperPageBase):
    def __init__(self, manager: ScraperSite, url: str):
        super().__init__(manager)
        self._response_content = self.get_response_content(url)

    @property
    def present_domain_zones(self) -> list:
        lst = []
        if self._response_content:
            page_soup = BeautifulSoup(self._response_content, 'lxml')
            box_header_soup = page_soup.select(".box-header")
            for item in box_header_soup:
                lst.append(item.text.strip())
        return lst


if __name__ == "__main__":
    scrape_site = ScraperSite()
    print(f"{scrape_site=}")
    print(f"{scrape_site.domains=}")
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


