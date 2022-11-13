# atm.py

import modules.database as db
import modules.ui as ui
import modules.utilites as util
import modules.matching_stack_bills as match_bills

VERSION_TOOL_STR = "ATM v 4.0 sqlite3 powered"


class ATM:
    """
    Клас, що забезпечує роботу з банкоматом
     * Починає роботу
     * Зберігає основті стани
     * До нього прив'язані всі інші елементи
    """
    def __init__(self, db_file_name):   
        db.prepare_db(db_file_name)
        self.conn = db.connect_db(db_file_name)
        self.add_atm_log("Розпочато роботу з банкоматом") 

        self.add_atm_log(f"Наповнюємоо касету банкомата даними із БД, балас \
банкомата:{db.get_db_atm_balance(self.conn)}")
        self.stack_atm = match_bills.create_stack_bills(
            db.get_db_banknotes(self.conn))
        # Ставорюємо касету клієнта (пусту)
        self.stack_user = match_bills.create_stack_bills()

    def start(self):
        """
        Початок роботи з банкоматом
        """
        print("Start Work ATM")
        start_menu = ui.StartMenu(
            self.conn, "Welcome", VERSION_TOOL_STR, 
            (("  1. | Login to ATM", "1", self.login_user), 
                ("  2. | Create new user", "2", self.create_user)))

        while True:
            _, choice, call_method = start_menu.show()
            if choice == 'x':
                break
            elif choice == 'z':
                continue
            call_method()

    def login_user(self):
        print("Початок аутентифікації користувача.")
        util.wait_key()

    def create_user(self):
        print("Початок створення нового користувача.")
        util.wait_key()

    def add_atm_log(self, message):
        db.add_log_atm(self.conn, message)

    def __del__(self):
        """
        Явне вивільнення ресурсів, при закінченні роботи із засобом
        """
        self.add_atm_log("Закінчено роботу з банкоматом")
        self.conn.close()
