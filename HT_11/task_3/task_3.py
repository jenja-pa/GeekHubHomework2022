# task_3.py
# 3. [X] Банкомат 4.0: 
#    - [X] переробити программу з функціонального підходу програмування на 
# використання класів; 
#    - [X] Додати шанс 10% отримати бонус на баланс при створенні нового 
# користувача.

from modules.atm import ATM

if __name__ == "__main__":
    atm = ATM("database.db")
    atm.start()
