# atm.py

import modules.database as db
import modules.ui as ui
import modules.utilites as utils
import modules.matching_stack_bills as match_bills


class ATM:
    """
    Клас, що забезпечує роботу з банкоматом
     * Починає роботу
     * Зберігає основті стани
     * До нього прив'язані всі інші елементи
    """
    version_str = "ATM v 4.0 -=- sqlite, OOP"
    
    def __init__(self, db_file_name):   
        db.prepare_db(db_file_name)
        self.conn = db.connect_db(db_file_name)
        self.user_info = None
        self.add_log("Розпочато роботу з банкоматом") 

        self.add_log(f"Наповнюємоо касету банкомата даними із БД, балас \
банкомата:{db.get_db_atm_balance(self.conn)}")
        self.stack_atm = match_bills.create_stack_bills(
            db.get_db_banknotes(self.conn))
        # Ставорюємо касету клієнта (пусту)
        self.stack_user = match_bills.create_stack_bills()

    def start(self):
        """
        Початок роботи з банкоматом
        """
        start_menu = ui.MenuStart(self)

        while True:
            _, choice, call_method = start_menu.show()
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
            elif input_value == "z":
                continue
            
            try:
                self.user_info = self.login_user_test(input_value)

                # Дії при успішному вході користувача
                # Отримати та встановити №сесії для користувача
                self.user_info["id_session"] = db.get_db_max_session4user_id(self.conn, self.user_info["id"]) + 1
                # handler admin
                self.add_log(f"Begin {self.user_info['name']} session. {'Administrator.' if self.user_info['permision'] & 1 == 1 else ''}")
                if self.user_info["permision"] & 1 == 1:
                    self.workflow_admin()
                else:
                    # simple user
                    self.workflow_user(self, self.user_info)
                self.add_log(f"End {self.user_info['name']} session.")
                # Прибираємо інформацію про користувача після закінчення роботи із ним, це вплаває на формування логу
                self.user_info = None
                break
            except ValueError as ex:
                self.add_log(f"Error input: {ex}")
                print(f"Error input: {ex}")
                utils.wait_key()

            except utils.UserLogonFalliedError as ex:
                self.add_log(f"Error authentication: {ex}")
                print(f"Error authentication: {ex}")
                utils.wait_key()

    def login_user_test(self, value):
        if len(value) == 0:
            raise ValueError("You entered empty value. Try again")
        if len(value.split()) < 2:
            raise ValueError("You entered only one values(need two separates by space).  Try again")
        
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
        print("Початок створення нового користувача.")
        utils.wait_key()

    def add_log(self, message):
        if self.user_info is None:
            # Сесія користувача не встановлена
            db.add_log_atm(self.conn, message)
        else:
            # Сесія користувача встановлена
            db.add_log_transaction(self.conn, self.user_info, message)

    def __del__(self):
        """
        Явне вивільнення ресурсів, при закінченні роботи із засобом
        """
        self.add_log("Закінчено роботу з банкоматом")
        self.conn.close()

    def workflow_admin(self):
        # self.conn, self.user_info
        print("Begin ADMIN workflow")
        utils.wait_key()

    def workflow_user(self):
        print("Begin USER workflow")
        utils.wait_key()
