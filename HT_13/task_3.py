# task_3.py
# Реалізуйте класс Transaction. Його конструктор повинен приймати такі 
# параметри:
#    - amount - суму на яку було здійснено транзакцію
#    - date - дату переказу
#    - currency - валюту в якій було зроблено переказ (за замовчуванням USD)
#    - usd_conversion_rate - курс цієї валюти до долара (за замовчуванням 1.0)
#    - description - опис транзакції (за дефолтом None)
#  Усі параметри повинні бути записані в захищені (_attr) однойменні атрибути.
#  Доступ до них повинен бути забезпечений лише на читання та за допомогою
# механізму property. 
#  При чому якщо description дорівнює None, то відповідне property має 
# повертати рядок "No description provided".
#  Додатково реалізуйте властивість usd, що має повертати суму переказу 
# у доларах (сума * курс)

class Transaction:
    def __init__(self, 
                 amount, 
                 date, 
                 currency="USD", 
                 usd_conversion_rate=1.0, 
                 description=None):
        self._amount = amount
        self._date = date
        self._currency = currency
        self._usd_conversion_rate = usd_conversion_rate
        self._description = description

    @property
    def amount(self):
        return self._amount

    @property
    def date(self):
        return self._date

    @property
    def currency(self):
        return self._currency

    @property
    def usd_conversion_rate(self):
        return self._usd_conversion_rate

    @property
    def description(self):
        if self._description is None:
            return "No description provided"
        return self._description

    @property
    def usd(self):
        if self._currency == "USD":
            return self._amount
        else:
            return float(round(self.amount * self.usd_conversion_rate, 2))


if __name__ == "__main__":
    print("Transaction 1")
    t1 = Transaction(1258.0, "25-11-2022", "GRN", 0.03565, "For support")
    print(f"{t1.amount=}")
    print(f"{t1.date=}")
    print(f"{t1.currency=}")
    print(f"{t1.usd_conversion_rate=}")
    print(f"{t1.description=}")
    print(f"{t1.usd=}")

    print()
    print("Transaction 2")
    t2 = Transaction(34.0, "24-11-2022")
    print(f"{t2.amount=}")
    print(f"{t2.date=}")
    print(f"{t2.currency=}")
    print(f"{t2.usd_conversion_rate=}")
    print(f"{t2.description=}")
    print(f"{t2.usd=}")

    print()
    print("Try change values")
    try:
        t1.amount = 4511.23
    except AttributeError as ex:
        print("Exception can't change amount:", ex)

    try:
        t1.date = "23-05-2021"
    except AttributeError as ex:
        print("Exception can't change date:", ex)

    try:
        t1.currency = "GBR"
    except AttributeError as ex:
        print("Exception can't change currency:", ex)

    try:
        t1.usd_conversion_rate = 0.58
    except AttributeError as ex:
        print("Exception can't change usd_conversion_rate:", ex)

    try:
        t1.description = "Sea cash"
    except AttributeError as ex:
        print("Exception can't change description:", ex)

