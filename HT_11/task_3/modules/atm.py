# atm.py

from datetime import datetime

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
        self.bonuses = {"new_user": (0.9, 55.99)}
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
            elif input_value == "":
                continue
            
            try:
                self.user_info = self.login_user_testing(input_value)

                # Дії при успішному вході користувача

                # Отримати та встановити №сесії для користувача
                self.user_info["id_session"] = db.get_db_max_session4user_id(self.conn, self.user_info["id"]) + 1

                self.add_log(f"Login user {self.user_info['name']} is successful.")
                # handler admin
                self.add_log(f"Begin {self.user_info['name']} session. {'Administrator.' if self.user_info['permision'] & 1 == 1 else ''}")
                if self.user_info["permision"] & 1 == 1:
                    self.workflow_admin()
                else:
                    # simple user
                    self.workflow_user()    
                self.add_log(f"End {self.user_info['name']} session.")
                # Прибираємо інформацію про користувача після закінчення роботи із ним, це вплаває на формування логу
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
        """Створення нового користувача ATM"""
        form_create_user = ui.InputCreateUser(self)
        while True:
            input_value = form_create_user.show()
            if input_value == "x":
                break
            elif input_value == "":
                continue
            
            try:    
                self.add_log(f"Testing entered user_name and password: ({input_value.split()[0]})")
                user_name, pwd = self.create_user_testing(input_value)

                # Дії при успішній перевірці даних нового користувача
                self.add_log(f"Try create new user: ({user_name})")
                print(f"Create user: {user_name}")
                db.set_db_new_user(self.conn, user_name, pwd)
                self.add_log(f"User: ({user_name}) - created successfuly.")
                
                db_users_info = db.get_db_users(self.conn)
                # нова фіча: 10% ймовірність бонусу на рахунок створеного користувача
                bonus = utils.ring_of_fotune_bonuses(self, "new_user")
                if bonus:
                    db.set_db_modify_user_balance(self.conn, db_users_info[user_name], bonus)
                    print(f"Congradulate. User: {user_name} win a bonus: {bonus:.2f} for registering")
                    self.add_log(f"You balance updated, you win a bonus: {bonus:.2f} for registering")
                    
                self.add_log(f"User: {user_name} is successfuly created.")
                print(f"User: {user_name} is successfuly created.")

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
                print("Fallied to create new user.", ex, "Try again another user.")
                self.add_log(f"Error: Fallied to create new user: {ex}")

            utils.wait_key()

    def create_user_testing(self, value):
        """Перевірка правильності введених імені та пароля нового користувача"""
        if len(value) == 0:
            raise ValueError("You entered empty value. Try again")
        if len(value.split()) < 2:
            raise ValueError("You entered only one values(need two separates by space).  Try again")

        user_name, pwd, *_ = value.split(" ")

        utils.validations_name_password(user_name, pwd)

        return (user_name, pwd)

    def workflow_admin(self):
        # self.conn, self.user_info
        print("Begin ADMIN workflow")
        menu_admin = ui.MenuAdmin(self)
        while True:
            _, choice, call_method = menu_admin.show()
            if choice == 'x':
                break
            elif choice == 'z':
                continue
            call_method()

    def menu_admin_change_cnt_of_banknotes(self):
        print("menu_admin_change_cnt_of_banknotes")
        utils.wait_key()

    def menu_admin_view_log(self):
        utils.clear_screen()
        print("Admin Log")
        print("Log transaction for All users and All time")
        print("-" * 40)

        for row in db.get_full_transaction(self.conn):
            str_date = datetime.strptime(
                row['date_time'], '%Y-%m-%d %H:%M:%S.%f')
            print(f"{str_date:%H:%M:%S} - {row['message']}")
        print("-" * 40)
        input("Move scrol up/down to see all log. Exit -> Press Enter")

        utils.wait_key()

    def workflow_user(self):
        print("Begin USER workflow")
        utils.wait_key()

    def add_log(self, message):
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

    def __del__(self):
        """
        Явне вивільнення ресурсів, при закінченні роботи із засобом
        """
        self.add_log("Закінчено роботу з банкоматом")
        self.conn.close()
