# task_2.py
# Програма для отримання курсу валют за певний період.
#  - отримати від користувача дату (це може бути як один день так і інтервал
#     - початкова і кінцева дати, продумайте механізм реалізації) 
#  - назву валюти
#  - вивести курс по відношенню до гривні на момент вказаної дати (або за кожен 
# день у вказаному інтервалі)
#  - не забудьте перевірку на валідність введених даних

# import json
# from os.path import exists
from datetime import datetime as dt, timedelta
from rich.prompt import Prompt
from rich.console import Console


from task_2_currency_exchange import CurrencyExchangeUAnbuScrapper
from task_2_rich_input import DatePromptCurrency


class CurrencyViewerApp:
    PATH_DATA_JSON = "task_2_currency.json"
    
    def __init__(self):
        # self._present_data = self.load_saved_data()
        self._present_data = {}
        self._get_remote_data = CurrencyExchangeUAnbuScrapper()
        now_str_date = dt.now().strftime('%d.%m.%Y')
        if now_str_date not in self._present_data.keys():
            currency_for_date = self._get_remote_data.get_site_currency_exchange_list(now_str_date)
            self._present_data[now_str_date] = currency_for_date

    # def load_saved_data(self):
    #     if exists(self.PATH_DATA_JSON):
    #         with open(self.PATH_DATA_JSON, encoding="utf-8") as f:
    #             return json.load(f)
    #     else:
    #         return {}
 
    # def save_present_data(self):
    #     with open(self.PATH_DATA_JSON, "w", encoding="utf-8") as f:
    #         json.dump(self._present_data, f)

    def get_data_for_date(self, str_date):
        # data = self._pre
        pass

    def get_seq_code_currence(self):
        str_date = dt.now().strftime('%d.%m.%Y')
        lst_exchange_date = self._present_data[str_date]["data"]
        lst_currensies = [item.char_code for item in lst_exchange_date]
        # print(f"get_seq_code_currence: {cur_date=}")
        return lst_currensies


if __name__ == "__main__":
    console = Console()
    str_today_date = dt.now().strftime('%d.%m.%Y')
    app = CurrencyViewerApp()
    print("Отримуємо курси валют за деякий період.")
    print(f"Дані отримані від https://bank.gov.ua/ за період з 02.09.1996 по "
          f"{str_today_date}")
    # print("Наявні коди валют для вибору:")
    # console.print("/".join(app.get_seq_code_currence()), style="red")
    str_code_currency = Prompt.ask(
        "Введіть одну із запропонованих валют для продовження:", 
        choices=app.get_seq_code_currence(), 
        default="USD")

    print("Ввести проміжок для аналізу, якщо потрібна одна дата ввести "
          "однакові значення.")
    str_date_beg = DatePromptCurrency.ask(
        "Введіть початкову дату (дд.мм.рррр):", 
        default=str_today_date)
    str_date_end = DatePromptCurrency.ask(
        "Введіть кінцеву дату (дд.мм.рррр):", 
        default=str_date_beg)

    date_beg = dt.strptime(str_date_beg, '%d.%m.%Y')
    date_end = dt.strptime(str_date_end, '%d.%m.%Y')
    if date_beg > date_end:
        raise ValueError(
            f"Помилкове задання проміжку початок {str_date_beg} "
            f"повиннен бути раніше за кінець {str_date_end}")

    delta = date_end - date_beg   # returns timedelta

    analise_data = []
    for i in range(delta.days + 1):
        day = date_beg + timedelta(days=i)
        str_date_need = day.strftime("%d.%m.%Y")
        # print(f"Get for date {str_date_need}")        
        data_need_all = app._get_remote_data.get_site_currency_exchange_list(
            str_date_need)["data"]
        # print(data_need_all)
        data_need = [
            item for item in data_need_all 
            if item.char_code == str_code_currency]
        analise_data.append((str_date_need, data_need[0]))

    print()
    print()
    # Out data
    print(f"Курс '{analise_data[0][1].description}' по відношенню до гривні")
    for date_item, item in analise_data:
        print(
            f"{date_item} : 1 {item.char_code} = {item.value / item.cnt:.6f} "
            f"грн.")

    # app.save_present_data()
