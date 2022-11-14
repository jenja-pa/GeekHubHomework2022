# ui.py
"""
Модуль, що надає можливості взаємодії з користувачем
 та виводить необхідну для роботи інформацію
"""

from itertools import chain as it_chain
from collections.abc import Iterable

import modules.database as db
import modules.utilites as utils


class Menu:
    def __init__(self, parent):
        self.parent = parent
        self.conn = parent.conn
        self.name = "Base empty menu"
        self.choice_items = ()

    def show(self):
        utils.clear_screen()
        look_title = f"""
#  {self.name} -=- {self.parent.version_str} 
-----------------------------------------
      ATM balance is: {db.get_db_atm_balance(self.conn):18.2f}   
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

        self.output_look((look_title, look_user_lst, look_footer))
        return self.logic()

    def output_look(self, look_items):
        look_title, look_user_lst, look_footer = look_items        
        max_len = self.get_max_length_seq(
            it_chain([
                look_title, 
                map(lambda item: item[0], look_user_lst), 
                look_footer]))

        self.out_prepare_look(look_title, max_len)
        self.out_prepare_look(look_user_lst, max_len)
        self.out_prepare_look(look_footer, max_len)

    def logic(self):
        press_key = None
        right_keys = list(map(
            lambda item: item[1], 
            it_chain(self.choice_items, (("", "x", ""),))))

        attemts = 0
        while (press_key := utils.wait_key("Select one of the item ...")) \
                not in right_keys and attemts < 3:
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
                
                if line[0] == "#":
                    print(f"#{line}{dummy[:-1]}##")
                else:
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
                if isinstance(line, str) and len(line) == 0:
                    continue
                current_len = self.get_max_length_seq(line)
                max_len = current_len if current_len > max_len else max_len
        else:
            raise TypeError(f"Error value: {strings} do not fits to work")
        return max_len


class MenuStart(Menu):
    def __init__(self, parent):
        super().__init__(parent)
        self.name = "Welcome"
        self.choice_items = (
            ("  1. | Login to ATM", "1", parent.login_user), 
            ("  2. | Create new user", "2", parent.create_user),
            )

    def show(self):
        utils.clear_screen()
        look_title = f"""
#  {self.name} -=- {self.parent.version_str} 
-----------------------------------------
      ATM balance is: {db.get_db_atm_balance(self.conn):18.2f}   
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

        self.output_look((look_title, look_user_lst, look_footer))
        return self.logic()


class MenuAdmin(Menu):
    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Admin menu"
        self.owner = owner
        self.choice_items = (
            ("  1. | Change count of banknotes", "1", owner.menu_admin_change_cnt_of_banknotes),
            ("  2. | View all ATM log", "2", owner.menu_admin_view_log),
            )

    def show(self):
        utils.clear_screen()
        look_title = f"""
# {self.name} -=- {self.parent.version_str} 
-----------------------------------------
  ATM balance is: {db.get_db_atm_balance(self.conn):.2f}
  Welcome user: {self.owner.user_info['name']} 
-----------------
""".strip() 

        look_user_lst = []
        for item in self.choice_items:
            look_user_lst.append(f"{item[0]}")

        look_footer = """ 
----------------
  x. | Exit menu
----------------
  """.strip()

        self.output_look((look_title, look_user_lst, look_footer))
        return self.logic()
    

class InputLoginUser(Menu):
    def __init__(self, parent):
        super().__init__(parent)
        self.name = "Login user"

    def show(self):
        utils.clear_screen()

        db_users = db.get_db_users(self.conn)
        avialible_users = ", ".join(map(lambda item: f'{item["name"]}/{item["password"]}' if item["name"] in ('admin', 'alex') else item["name"], db_users.values()))

        look_title = f"""
#  {self.name} -=- {self.parent.version_str} 
-----------------------------------------
Avalible users: {avialible_users}
-------
Prease enter user and password separated by space (enter x to exit):
-------        
""".strip()

        self.output_look((look_title, "", ""))
        value = input("> ").strip()

        return value


class InputCreateUser(Menu):
    def __init__(self, parent):
        super().__init__(parent)
        self.name = "Create user"

    def show(self):
        utils.clear_screen()
        look_title = f"""
#  {self.name} -=- {self.parent.version_str} 
-----------------------------------------
Create new user for ATM. You have a chance win a bonuse.
-------     
Restriction:
  user 
  * must have a length 3..50 chars
  * contain: 
    - latin letters, digits, and symbols _ -
  * do not start from digits   
  password
  * must have a length longest 7 chars
  * contain: 
    - latin letters, digits, and symbols _
    - contain least one - digit, latin letters in upper and lower registry
------
Prease enter user and password separated by space (enter x to exit):
------------
""".strip()
        self.output_look((look_title, "", ""))
        value = input("> ").strip()

        return value


#     print(f"""
# ## Login -=- ATM v 3.0 sqlite3 powered                         ##
# #        You have try {attempts:>2} attempts to enter                     ##
# -----------------------------------------------------------------
# # Present users: {avialible_users}
# #----------------------------------------------------------------
# """)

