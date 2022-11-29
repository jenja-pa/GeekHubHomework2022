# atm.py

import traceback

from datetime import datetime

import modules.database as db
import modules.ui as ui
import modules.utilites as utils
import modules.atm_get_bills_dyn as match_bills
import modules.currency_exchange as currency_exchange


class ATM:
    """
    Клас, що забезпечує роботу з банкоматом
     * Починає роботу
     * Зберігає основті стани
     * До нього прив'язані всі інші елементи
    """
    version_str = "ATM v 5.0 -=- sqlite, OOP, requests"
    
    def __init__(self, db_file_name, bonuses={}):   
        db.prepare_db(db_file_name)
        self.conn = db.connect_db(db_file_name)
        self.user_info = None
        self.bonuses = bonuses
        self.add_log("Розпочато роботу з банкоматом") `

        self.add_log(f"Наповнюємоо касету банкомата даними із БД, балас" 
                     f"банкомата:{db.get_db_atm_balance(self.conn)}")
        self.stack_atm = match_bills.create_stack_bills(
            db.get_db_bills(self.conn))
        # Ставорюємо касету клієнта (пусту)
        self.stack_user = match_bills.create_stack_bills()

    def start(self):
        """
        Початок роботи з банкоматом
        """
        start_menu = ui.MenuStart(self)

        while True:
            _, choice, call_method, *_ = start_menu.show()
            if choice == 'x':
                break
            elif choice == 'z':
                continue
            call_method()

    def login_user(self):
        form_login = ui.InputLoginUser(self)
        while True:
            input_value = form_login.show()
            if input_value == "x":
                break
            elif input_value == "":
                continue
            
            try:
                self.user_info = self.login_user_testing(input_value)
                # Отримати та встановити №сесії для користувача
                self.user_info["id_session"] = db.get_db_max_session4user_id(
                    self.conn, self.user_info["id"]) + 1

                # Дії при успішному вході користувача
                self.add_log("#")
                flag = None
                if self.user_info['permision'] & 1 == 1:
                    flag = 'Administrator.' 
                else:
                    flag = ''
                self.add_log(
                    f"Begin user:{self.user_info['name']} session. {flag}")
                if self.user_info["permision"] & 1 == 1:
                    # handler admin
                    self.workflow_admin()
                else:
                    # simple user
                    self.workflow_user()    
                self.add_log(f"End user:{self.user_info['name']} session.")
                self.add_log("#")
                # Прибираємо інформацію про користувача після закінчення 
                # роботи із ним, це вплаває на формування логу
                self.user_info = None
                break
            except ValueError as ex:
                self.add_log(f"Error input: {ex}")
                print(f"Error input: {ex}")
                utils.wait_key()

            except db.UserLogonFalliedError as ex:
                self.add_log(f"Error authentication: {ex}")
                print(f"Error authentication: {ex}")
                utils.wait_key()

    def login_user_testing(self, value):
        if len(value) == 0:
            raise ValueError("You entered empty value. Try again")
        if len(value.split()) < 2:
            raise ValueError("You entered only one values(need two separates" 
                             "by space). Try again")
        
        user, pwd, *_ = value.split(" ")
        dct_users = db.get_db_users(self.conn)

        # test user and password
        if dct_users.get(user, None) is None:
            raise db.UserLogonFalliedError(
                f"Entered user: {user}, are not avialible")
        if dct_users[user]["password"] != pwd:
            raise db.UserLogonFalliedError(
                f"Entered password for user: {user} are wrong")

        return dct_users[user]

    def create_user(self):
        """Створення нового користувача ATM"""
        form_create_user = ui.InputCreateUser(self)
        while True:
            input_value = form_create_user.show()
            if input_value == "x":
                break
            elif input_value == "":
                continue
            
            try:    
                self.add_log(f"Testing entered user_name and password:"
                             f"({input_value.split()[0]})")
                user_name, pwd = self.create_user_testing(input_value)

                # Дії при успішній перевірці даних нового користувача
                self.add_log(f"Try create new user: ({user_name})")
                print(f"Create user: {user_name}")
                db.set_db_new_user(self.conn, user_name, pwd)
                
                db_users_info = db.get_db_users(self.conn)
                self.add_log(f"User: ({user_name}) - created successfuly.")
                # нова фіча: 10% ймовірність бонусу на рахунок створеного 
                # користувача
                bonus = utils.ring_of_fotune_bonuses(self, "new_user")
                if bonus:
                    db.set_db_modify_user_balance(
                        self.conn, db_users_info[user_name], bonus)
                    tmp_message = f"Congradulate. User: {user_name} win " \
                                  f"a bonus: {bonus:.2f} for registering"
                    print(tmp_message)
                    # print(f"{db_users_info=}")
                    db_users_info[user_name]["id_session"] = \
                        db.get_db_max_session4user_id(
                            self.conn, 
                            db_users_info[user_name]["id"]) + 1
                    self.add_user_log(db_users_info[user_name], tmp_message)
                    
                utils.wait_key()
                break
            except ValueError as ex:
                print(ex, "Try again.")
                self.add_log(f"Error: {ex}")
            except utils.NameIncorrectException as ex:
                print("User name is incorrect.", ex, "Try again.")
                self.add_log(f"Error: User name is incorrect: {ex}")
            except utils.PasswordIncorrectException as ex:
                print("Password is incorrect.", ex, "Try again.")
                self.add_log(f"Error: Password is incorrect: {ex}")
            except db.Error as ex:
                print(
                    "Fallied to create new user.", ex, 
                    "Try again another user.")
                self.add_log(f"Error: Fallied to create new user: {ex}")

            utils.wait_key()

    def create_user_testing(self, value):
        """
        Перевірка правильності введених імені та пароля нового користувача
        """
        if len(value) == 0:
            raise ValueError("You entered empty value. Try again")
        if len(value.split()) < 2:
            raise ValueError("You entered only one values(need two separates"
                             "by space).")

        user_name, pwd, *_ = value.split(" ")

        utils.validations_name_password(user_name, pwd)

        return (user_name, pwd)

    def view_currency_tables(self):
        """Показ доступнгих таблиць курсів валют"""
        menu_choice = ui.MenuCurrencyTables(self)

        while True:
            _, choice, call_method, *_ = menu_choice.show()
            if choice == 'x':
                break
            elif choice == 'z':
                continue
            call_method()

    def view_currency_nbu_table(self):
        """Показ поточного курсу валют від нацбанку"""
        # В подальшому бажано підключити отримання даних від декількох джерел 
        # - зараз буде тільки НБУ
        utils.clear_screen()
        scrapper = currency_exchange.TodayCurrencyExchangeUAnbuScrapper()
        data_currency = scrapper.get_site_currency_exchange_list()
        if data_currency is None:
            print("Не вдалося отримати дані. Спробуйте пізніше.")
            utils.wait_key()
        else:
            print()
            print(f'Курси валют НБУ на {data_currency["date_txt"]}')
            print("-" * 29)
            print(
                f'{data_currency["header"][0][:7]:7}.|'
                f'{data_currency["header"][1][:7]:7}.|кільк.|'
                f'{data_currency["header"][3]:40}|  Грн.')
            print("-" * 74)
            for row in data_currency["data"]:
                print(f"   {row.int_code:03}  |{row.char_code:^8}|{row.cnt:6}"
                      f"|{row.description:40}|{row.value:>8.4f}")
            print("-" * 74)
            print()
            mess = "Look information <Enter> to Exit"
            input(f"{' ' * ((74 - len(mess)) // 2)}{mess}")

    def view_currency_pb_table(self):
        """Показ поточного курсу валют від Приват """
        # В подальшому бажано підключити отримання даних від декількох джерел 
        # - зараз буде тільки НБУ
        utils.clear_screen()
        scrapper = currency_exchange.CurrencyExchangePbScrapper()
        data_currency = scrapper.currency_exchange_list()
        if data_currency is None:
            print("Не вдалося отримати дані. Спробуйте пізніше.")
            utils.wait_key()
        else:
            print()
            print(f'Курси валют ПриватБанк на {data_currency["date_txt"]}')
            print("-" * 36)
            print("|".join(data_currency["header"]))
            print("-" * 89)
            for row in data_currency["data"]:
                # print(f"{row=}")
                print(f"   {row.int_code:03}  |{row.char_code:^8}|{row.cnt:6}"
                      f"|{row.description:40}|{row.value:>11.4f}|"
                      f"{row.value_sale:>11.4f}")
            print("-" * 89)
            print()
            mess = "Look information <Enter> to Exit"
            input(f"{' ' * ((89 - len(mess)) // 2)}{mess}")

    def workflow_admin(self):
        """
        Робочий процес адміністратора
        """
        menu_admin = ui.MenuAdmin(self)
        while True:
            _, choice, call_method, *_ = menu_admin.show()
            if choice == 'x':
                break
            elif choice == 'z':
                continue
            call_method()

    def menu_admin_change_cnt_of_bills(self):
        """
        Перегляд модифікація наявності купюр у банкоматі
        """
        menu_choice = ui.MenuChangeCntBills(self)
        self.add_log("Початок роботи зі зміни кількості банкнот:")
        while True:
            _, key, call_method, nominal = menu_choice.show()
            if key == 'x':
                break
            elif key == 'z':
                continue
            try:
                stack_atm = db.get_db_bills(self.conn)
                new_cnt = call_method(nominal)
                self.add_log(f"Змінено кількість банкнот '{nominal}' з "
                             f"{stack_atm[nominal]} на {new_cnt}")
                continue
            except ValueError as ex:
                print(f"Error: {ex}")
                self.add_log(f"Помилка зміни кількості банкнот '{nominal}' "
                             f"з {stack_atm[nominal]} на {new_cnt}")
        self.add_log("Кінець роботи зі зміни кількості банкнот.")

    def menu_admin_operation_change_cnt_of_bills(self, nominal):
        """Функція, що змінює поточну кількість банкнот"""
        try:
            value = utils.input_int(f"Enter new value of bills '{nominal}': ")
            db.set_db_bills_count(self.conn, self.user_info, nominal, value)
            self.add_log(f"Change count of '{nominal}' bills to {value}")
        except ValueError as ex:
            self.add_log(f"Проблема зміни кількості банкнот '{nominal}' "
                         f"to {value}. {ex}")
            print(f"Проблема зміни кількості банкнот '{nominal}' "
                  f"to {value}. {ex}")
            utils.wait_key()

    def menu_admin_view_log(self):
        utils.clear_screen()
        print("Admin Log")
        print("Log combined with ATM and users, for all")
        print(utils.align_center("-" * (utils.get_terminal_size() - 8)))

        for row in db.get_full_transaction(self.conn):
            str_date = datetime.strptime(
                row['date_time'], '%Y-%m-%d %H:%M:%S.%f')
            prepare_string = f"{str_date:%H:%M:%S} : {row['user_name']} - " \
                             f"{row['message']}"
            print(utils.shorting_string(prepare_string.strip()))
        print(utils.align_center("-" * (utils.get_terminal_size() - 8)))

        input(utils.align_center('Move scrol up/down to see all log. '
                                 'Exit -> Press Enter'))

    def workflow_user(self):
        """
        Робочий процес простого користувача
        """
        menu_user = ui.MenuUser(self)
        while True:
            _, choice, call_method, *_ = menu_user.show()
            if choice == 'x':
                break
            elif choice == 'z':
                continue
            call_method()

    def menu_user_deposit_account(self):
        """
        Поповнення рахунку користувачем
        """
        min_nominals = min(
            item for item in db.get_db_bills(self.conn).keys())

        try:
            value = utils.input_float(
                "Please enter sum that you want take to deposite (float): ")
            if value < 0:
                raise ValueError(
                    f"Sorry value of funds must be larger zero "
                    f"not {value:.2f}")
        except ValueError as ex:
            print(ex)
            utils.wait_key()
            return

        self.add_log(f"User: {self.user_info['name']} want "
                     f"to deposit {value:.2f}$ ")

        real_value_to_deposit = (value // min_nominals) * min_nominals

        db.set_db_modify_user_balance(
            self.conn, self.user_info, real_value_to_deposit)
        self.add_log(f"for user: {self.user_info['name']}:"
                     f"{self.user_info['balance']:.2f} "
                     f"make accruals {real_value_to_deposit:.2f}$ "
                     f"and change: "
                     f"{round(value - real_value_to_deposit, 2):.2f}")
        self.user_info["balance"] += real_value_to_deposit

        print(f"You provided: {value:.2f}$, enrolled: "
              f"{real_value_to_deposit:.2f}$, change: "
              f"{round(value - real_value_to_deposit, 2)}$")
        utils.wait_key()

    def menu_user_withdraw_funds(self):
        """Зняття коштів користувачем"""
        try:
            value = utils.input_float(
                "Please enter sum that you want to withdraw (float): ")
            if value < 0:
                raise ValueError(f"Sorry value of funds must be larger "
                                 f"zero not {value:.2f}")
        except ValueError as ex:
            print(ex)
            utils.wait_key()
            return

        # Введену суму вирівняти на Мінімально можливий номінал
        min_nominal = min(
            item for item in db.get_db_bills(self.conn).keys())
        value = int((value // min_nominal) * min_nominal)

        atm_balance = db.get_db_atm_balance(self.conn)
        user_balance = self.user_info["balance"]
        self.add_log(
            f"User: {self.user_info['name']} want to withdraw {value:.2f}$. "
            f"From your account: {user_balance:.2f}$")
        try:
            if value > user_balance:
                self.add_log(
                    f"Refused. Withdraw {value:.2f}$. Overbalance your "
                    f"account: {user_balance:.2f}$")
                raise ValueError(
                    f"Sorry. Your balance: {user_balance}$ does not allow "
                    f"withdraw {value}$")
            if value > atm_balance:
                self.add_log(
                    f"Refused. Withdraw {value:.2f}$. Overbalance the ATM "
                    f"account: {atm_balance:.2f}$")
                raise ValueError(
                    f"Sorry. ATM has: {atm_balance}$ only does not allow "
                    f"withdraw {value}$")

            self.add_log(
                f"Accepted to withdraw. User: {self.user_info['name']} "
                f"get {value:.2f}$ from balance: {user_balance:.2f}$")
            # Провести генераціюб банкнот до видачі
            stack_atm = match_bills.create_stack_bills(
                db.get_db_bills(self.conn))
            try:
                stack_user = match_bills.form_apropriate_stack_dyn(
                    value, 
                    stack_atm
                    ) 
                # Зміна баланса користувача
                db.set_db_modify_user_balance(
                    self.conn, self.user_info, -value)
                # Зміна кількості банкнот в ATM та занесення змін у БД
                for nominal in stack_user:
                    if stack_user[nominal] > 0:
                        db.set_db_bills_count(
                            self.conn, self.user_info, nominal, 
                            stack_atm[nominal] - stack_user[nominal])
                print(f"You want to take off {value}.")
                print("You given out bills: ", end="")
                lst = [
                    f"{cnt}*{nominal}" for nominal, cnt in 
                    filter(lambda item: item[1] > 0,  stack_user.items())]
                print(", ".join(lst))
                self.add_log(
                    f"You given: {value} with next bills: [{', '.join(lst)}]")
                self.user_info["balance"] -= value
                self.add_log(f"New balance is {self.user_info['balance']:.2f}")
            except ValueError as ex:
                self.add_log(
                    f"Refused. Withdraw {value:.2f}$ "
                    f"to user:{self.user_info['name']}. {ex}")
            except Exception:
                print(str(traceback.format_exc()))

            self.add_log(
                f"User: {self.user_info['name']} new balance: "
                f"{round(user_balance - value, 2):.2f}$")

        except ValueError as ex:
            print("Error.", ex)
        else:
            print("Operation Withdraw_funds - Success")
        utils.wait_key()

    def menu_user_view_log(self):
        """
        Видача логу для даного користувача
        """
        utils.clear_screen()
        print(f"Log transaction for user:{self.user_info['name']}")
        print(utils.align_center("-" * (utils.get_terminal_size() - 6)))

        rows = db.get_transaction(self.conn, self.user_info)

        for row in rows:
            prepare_date = datetime.strptime(
                row['date_time'], '%Y-%m-%d %H:%M:%S.%f')

            print(f"{row['id_session']:4} : {prepare_date:%d.%m.%Y %H:%M:%S}"
                  f" - {row['message']}")
        print(utils.align_center("-" * (utils.get_terminal_size() - 6)))
        input(utils.align_center(
            "Move scrol up/down to see all log. Exit -> Press Enter"))

    def add_log(self, message):
        """
        Запис у лог беручи до уваги поточно вибраного користувача
        (Простий варіант)
        """
        if self.user_info is None:
            # інформація про користувача не встановлена
            db.add_log_atm(self.conn, message)
        elif self.user_info.get("id_session", None) is None:        
            # Сесія користувача не встановлена
            db.add_log_atm(self.conn, message)
        elif self.user_info.get("permision", None) != 0:
            # Користувач з правами адміністратора
            db.add_log_atm(self.conn, message)
        else:
            # Сесія користувача встановлена
            db.add_log_transaction(self.conn, self.user_info, message)

    def add_user_log(self, user_info, message):
        """
        Запис у лог із примусово встановленими даними про користувача
        """
        db.add_log_transaction(self.conn, user_info, message)

    def __del__(self):
        """
        Явне вивільнення ресурсів, при закінченні роботи із засобом
        """
        self.add_log("Закінчено роботу з банкоматом")
        self.conn.close()
