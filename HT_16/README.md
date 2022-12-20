# HT_16

1. :white_check_mark: Використовуючи Scrapy, заходите на "https://chrome.google.com/webstore/sitemap", переходите на кожен лінк з тегів <loc>, з кожного лінка берете посилання на сторінки екстеншинів, парсите їх і зберігаєте в CSV файл ID, назву та короткий опис кожного екстеншена (пошукайте уважно де його можна взяти). 

> Наприклад:
```
“aapbdbdomjkkjkaonfhkkikfgjllcleb”, 
“Google Translate”, 
“View translations easily as you browse the web. By the Google Translate team.”
```

2. :white_check_mark: Викорисовуючи Scrapy, написати скрипт, який буде приймати на вхід назву та ID категорії (у форматі назва/id/) із сайту https://rozetka.com.ua і буде збирати всі товари із цієї категорії, збирати по ним всі можливі дані (бренд, категорія, модель, ціна, рейтинг тощо) і зберігати їх у CSV файл 
> (наприклад, якщо передана категорія mobile-phones/c80003/, то файл буде називатися c80003_products.csv)

П.С. Запуск кожного процесу відбувається шляхом запуску відповідного файлу task.py (як до цього запускалися попередні домашки), а не через консоль (гугл підкаже how to start scrapy programmatically :wink:)

П.С.С У завданні 2 назву категорії просто збережіть у змінну (не треба робити через input())

Приклади emoji :white_check_mark: :black_square_button: :heavy_check_mark: :o: :x: :radio_button:
