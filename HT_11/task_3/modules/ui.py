# ui.py
"""
Модуль, що надає можливості взаємодії з користувачем
 та виводить необхідну для роботи інформацію
"""

from itertools import chain as it_chain
from collections.abc import Iterable

import modules.database as db
import modules.utilites as util


class Menu:
    def __init__(self, name="", version_str=""):
        self.title = f"{name} -=- {version_str}"
        self.info = ""
        self.user_items = []

        self.live_data = {}

    def show(self):
        pass

    def refresh(self):
        pass

    def out_prepare_look(self, look, max_length):
        if isinstance(look, str):
            self.out_prepare_str(look, max_length)
        elif isinstance(look, Iterable):
            for lines in look:
                self.out_prepare_str(lines, max_length)
        else:
            raise TypeError(
                "Sorry type of parameter must be a string or be an iterable")
   
    def out_prepare_str(self, line, max_length):
        if isinstance(line, str):
            for line in line.splitlines():
                if line.startswith("---"):
                    dummy = "-" * (max_length - len(line))    
                else:
                    dummy = " " * (max_length - len(line))
                print(f"#{line}{dummy}#")
        else:
            raise TypeError("Sorry type of parameter must be a string")

    def get_max_length_seq(self, strings):
        """
        Визначення максимальної довжини рядка, для проведення 
        подальшого оформлення

        Вважаємо, що надані рядки також можуть бути багатостроковими

        Return
        ------
            length of max wide string
        """
        max_len = 0
        if isinstance(strings, str):
            current_len = max(len(item) for item in strings.splitlines())
            max_len = current_len if current_len > max_len else max_len
        elif isinstance(strings, Iterable):
            for line in strings:
                current_len = self.get_max_length_seq(line)
                max_len = current_len if current_len > max_len else max_len
        else:
            raise TypeError(f"Error value: {strings} do not fits to work")
        return max_len


class StartMenu(Menu):
    def __init__(self, conn, name="", version_str="", choice_items=()):
        self.name = name
        self.version_str = version_str
        self.choice_items = choice_items
        self.conn = conn

    def show(self):
        util.clear_screen()
        look_title = f"""
# {self.name} to {self.version_str} 
-----------------------------------------
      ATM balance is: {db.get_db_atm_balance(self.conn):18.2f}   
-----------------------------------------
 key | Description
-----------------------------------------
""".strip()
        
        look_user_lst = []
        for item in self.choice_items:
            look_user_lst.append(f"{item[0]}")

        look_footer = """ 
----------------
  x. | Exit menu
----------------
  """.strip()

        max_len = self.get_max_length_seq(
            it_chain([
                look_title, 
                map(lambda item: item[0], look_user_lst), 
                look_footer]))

        self.out_prepare_look(look_title, max_len)
        self.out_prepare_look(look_user_lst, max_len)
        self.out_prepare_look(look_footer, max_len)

        press_key = None
        right_keys = list(map(
            lambda item: item[1], it_chain(self.choice_items, (("", "x", ""),))))

        attemts = 0
        while (press_key := 
               util.wait_key("Select one of the item ...")) not in right_keys and attemts < 3:
            print(f"Sorry {press_key} is a wrong key.")
            attemts += 1

        if attemts >= 3:
            return ("", "z", "")
        if press_key.lower() == 'x':
            return ("", 'x', "")
        result = tuple(filter(
            lambda item: item[1] == press_key.lower(), 
            self.choice_items))
        return result[0]


class FormLoginMenu:
    def __init__(self, name="Welcome", version_str=""):
        pass

    # choice_menu(

# f"""
# ## Welcome to ATM v 3.0 sqlite3 powered ##
# #-----------------------------------------
# #      ATM balance is: {db.get_db_atm_balance(conn):.2f}
# #-----------------------------------------
# # key | Description
# #-----------------------------------------""", (
#         ("#  1. | Create new user", "1", create_new_user),
#         ("#  2. | Login to ATM", "2", login_user),
#         ("# ", None, None),
#         ("#  x. | Exit", "x", exit_atm)
#     ), """#-----------------------------------------""")

