# task_1.py
# Задача Банкомат 5.0
#     Додати до банкомату меню отримання поточного курсу валют за допомогою 
# requests (можна використати відкрите API ПриватБанку)
from modules.atm import ATM

if __name__ == "__main__":
    bonuses = {"new_user": (0.1, 50.00)}
    atm = ATM("database.db", bonuses=bonuses)
    atm.start()
