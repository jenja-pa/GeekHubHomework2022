# HT 17
Автоматизувати процес замовлення робота за допомогою Selenium
1. :white_check_mark: Отримайте та прочитайте дані з "https://robotsparebinindustries.com/orders.csv". 
Увага! Файл має бути прочитаний з сервера кожного разу при запускі скрипта, 
не зберігайте файл локально.
2. :white_check_mark: Зайдіть на сайт "https://robotsparebinindustries.com/"
3. :white_check_mark: Перейдіть у вкладку "Order your robot"
4. :white_check_mark: Для кожного замовлення з файлу реалізуйте наступне:
    - :white_check_mark: закрийте pop-up, якщо він з'явився. Підказка: не кожна кнопка його закриває.
    - :white_check_mark: оберіть/заповніть відповідні поля для замовлення
    - :white_check_mark: натисніть кнопку Preview та збережіть зображення отриманого робота. Увага! Зберігати треба тільки зображення робота, а не всієї сторінки сайту.
    - :white_check_mark: натисніть кнопку Order та збережіть номер чеку. Увага! Інколи сервер тупить і видає помилку, але повторне натискання кнопки частіше всього вирішує проблему. Дослідіть цей кейс.
    - :white_check_mark: переіменуйте отримане зображення у формат <номер чеку>_robot. Покладіть зображення в директорію output (яка має створюватися/очищатися під час запуску скрипта).
    - :white_check_mark: замовте наступного робота (шляхом натискання відповідної кнопки)
5. :black_square_button: Створити лог виконання роботи
6. :black_square_button: Для загального розуміння можна переглянути відео https://www.youtube.com/watch?v=0uvexJyJwxA&ab_channel=Robocorp

7. black_square_button: Додаткове завдання (необов'язково)
  - окрім збереження номеру чеку збережіть також HTML-код всього чеку
  - збережіть отриманий код в PDF файл
  - додайте до цього файлу отримане зображення робота (бажано на одній сторінці, але не принципово)
  - збережіть отриманий PDF файл у форматі <номер чеку>_robot в директорію output. Окремо зображення робота зберігати не потрібно. (edited) 
	
>	аргументи для хром опцій
```
[
            '--no-sandbox',
            '--disable-web-security',
            '--allow-running-insecure-content',
            '--hide-scrollbars',
            '--disable-setuid-sandbox',
            '--profile-directory=Default',
            '--ignore-ssl-errors=true',
            '--disable-dev-shm-usage'
]
```

> експериментальні опції
```
'excludeSwitches', ['enable-automation']
'prefs', {
                'profile.default_content_setting_values.notifications': 2,
                'profile.default_content_settings.popups': 0
            }
```
