#HT 19

##На основі скрейпера із ДЗ №15 написати сайт із наступним функціоналом:

1. :black_square_button: Сторінка "Додати продукти", на якій буде textfield, в який можна ввести будь-яку кількість ID продуктів. 
2. :black_square_button: При відправленні форми повинен запуститись скрейпер і зібрати всі продукти із обраними ID з сайту Розетки.
3. :black_square_button: Сторінка "Мої продукти", на якій вивести всі продукти, які є в системі, із зазначенням їхніх основних параметрів (назва, ціна).
4. :black_square_button: Сторінка "Продукт", на якій будуть виведені вся інформація про обраний продукт: назва, ціна, ІД, короткий опис (якщо є), бренд, категорія, лінка на продукт (на сайті Розетки) і т.д.

P.S. Процес скрейпінга повинен відбуватись "на бекграунді" - тобто основний потік виконання не повинен блокуватись. 
Варіант вирішення цієї задачі: використовувати додаткову модель, наприклад, ScrapingTask, в яку запишется значення textfield. 
А отриманий ID цієї таски при запуску скрейпера в сабпроцесі передати в якості параметра.

:black_square_button: :white_check_mark: