# task_3.py
# http://quotes.toscrape.com/ - написати скрейпер для збору всієї доступної 
# інформації про записи: 
#     цитата, автор, інфа про автора тощо.
#  - збирається інформація з 10 сторінок сайту.
#  - зберігати зібрані дані у CSV файл
import csv
from dataclasses import dataclass, fields, astuple
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

import os.path


@dataclass
class Quote:
    text: str
    author_name: str
    link_author: str
    tags: [str]


@dataclass
class Author:
    author_name: str
    date_born_str: str
    place_born: str
    description: str


class QuotesScrapper:
    """Класс для збору інформації із ресурсу quotes.toscrape.com"""
    BASE_URL = "http://quotes.toscrape.com/"
    CSV_OUTPUT_PATH = ''

    def __init__(self):
        self._quotes = []
        self._authors = {}
    
    def get_quote_pages(self):
        """Основна обробка сторінок сайту"""
        print(f"Get: {self.BASE_URL}")
        response = requests.get(self.BASE_URL)
        if not response.ok:
            print(f"Error request, code:{response.code}")
            return

        while True:
            page = response.content
            page_soup = BeautifulSoup(page, 'lxml')
            
            # робота із сторінкою
            for quot_soup in page_soup.select(".quote"):
                data_quote = self.parse_quote_soup(quot_soup)
                self._quotes.append(data_quote)
                if data_quote.author_name not in self._authors:
                    author_soup = self.get_author_page_soup(
                        data_quote.link_author)
                    data_author = self.parse_author_soup(
                        author_soup.select_one("div.author-details"))
                    self._authors[data_quote.author_name] = data_author

            # Перевірка, що це остання сторінка
            if page_soup.select_one(".next") is None:
                return "Work scraping data ended"

            url_to_next = urljoin(
                self.BASE_URL, 
                page_soup.select_one(".next a")["href"])
            print(f"Get: {url_to_next}")
            response = requests.get(url_to_next)
            if not response.ok:
                print(f"Error request, code:{response.code}")
                return

    def parse_quote_soup(self, quot_soup):
        return Quote(
            text=quot_soup.select_one("span.text").text,
            author_name=quot_soup.select_one("small.author").text,
            link_author=quot_soup.select_one("div span a")["href"],
            tags=[item.text for item in quot_soup.select("div.tags a.tag")]
            )

    def get_author_page_soup(self, link) -> BeautifulSoup:
        url_to_get = urljoin(self.BASE_URL, link)
        print(f"Get author detail: {url_to_get}")
        response = requests.get(url_to_get)
        if not response.ok:
            print(f"Error request: {url_to_get}, code:{response.code}")
            return        

        return BeautifulSoup(response.content, 'lxml')

    def parse_author_soup(self, author_soup) -> Author:
        return Author(
            author_name=author_soup.select_one(".author-title").text.strip(),
            date_born_str=author_soup.select_one("span.author-born-date").text,
            place_born=author_soup.select_one(
                "span.author-born-location").text,
            description=author_soup.select_one(
                "div.author-description").text.strip()
            )

    def write_quotes_csv(self, f_name: str) -> None:
        field_names = [field.name for field in fields(Quote)]
        f_full_path = os.path.join(self.CSV_OUTPUT_PATH, f_name)
        with open(f_full_path, 'w', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(field_names)
            writer.writerows([astuple(quote) for quote in self._quotes])
        return

    def write_authors_csv(self, f_name):
        field_names = [field.name for field in fields(Author)]
        f_full_path = os.path.join(self.CSV_OUTPUT_PATH, f_name)
        with open(f_full_path, 'w', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(field_names)
            writer.writerows(
                [astuple(quote) for quote in self._authors.values()])
        return


if __name__ == "__main__":
    scraper = QuotesScrapper()
    result = scraper.get_quote_pages()
    print(result)
    # print(f"{scraper._quotes}")
    scraper.write_quotes_csv("task_3_quotes.csv")
    scraper.write_authors_csv("task_3_authors.csv")
