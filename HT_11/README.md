# HT 11
1. [X] Створити клас Calc, який буде мати атребут last_result та 4 методи. Методи повинні виконувати математичні операції з 2-ма числами, а саме додавання, віднімання, множення, ділення.
   - [X] Якщо під час створення екземпляру класу звернутися до атрибута last_result він повинен повернути пусте значення.
   - [X] Якщо використати один з методів - last_result повинен повернути результат виконання ПОПЕРЕДНЬОГО методу.
   ```
   Example:
    last_result --> None
    1 + 1
    last_result --> None
    2 * 3
    last_result --> 2
    3 * 4
    last_result --> 6
    ...
   ```
   - [X] Додати документування в клас (можете почитати цю статтю: 
https://realpython.com/documenting-python-code/ )

2. [X] Створити клас Person, в якому буде присутнім метод \_\_init\_\_ який 
буде приймати якісь аргументи, які зберігатиме в відповідні змінні.
   - [x] Методи, які повинні бути в класі Person 
         - show_age, print_name, show_all_information.
   - [x] Створіть 2 екземпляри класу Person та в кожному з екземплярів створіть
атрибут profession (його не має інсувати під час ініціалізації в самому класі) 
та виведіть його на екран (прінтоніть)

3. [X] Банкомат 4.0: 
   - [X] переробити программу з функціонального підходу програмування на використання класів; 
   - [X] Додати шанс 10% отримати бонус на баланс при створенні нового користувача.
