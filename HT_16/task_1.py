# task_1.py
# Використовуючи Scrapy, заходите на 
#   "https://chrome.google.com/webstore/sitemap", 
# переходите на кожен лінк з тегів , з кожного лінка берете посилання на 
# сторінки екстеншинів, парсите їх і зберігаєте в CSV файл:
#  * ID, 
#  * назву, 
#  * короткий опис кожного екстеншена (пошукайте уважно де його можна взяти).
# 
# Наприклад:
# “aapbdbdomjkkjkaonfhkkikfgjllcleb”, 
# “Google Translate”, 
# “View translations easily as you browse the web. By the Google Translate ...”

from scrapy_crawlers.run_spider_chrome_webstore import run_spider

if __name__ == "__main__":
    run_spider("scrapy_crawlers")
