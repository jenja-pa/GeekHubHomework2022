# task_2_rich_input.py
from rich.prompt import PromptBase
from rich.prompt import InvalidResponse
from rich.console import Console

# import rich.prompt
from datetime import datetime as dt

console = Console()


class DatePromptCurrency(PromptBase):
    """Ввід дати у форматі dd.mm.yyyy у проміжку від 02.09.1996 по сьогодні

    Приклад застосування:
    date_inp = DatePromptCurrency.ask(
        "Enter date begin:(dd.mm.yyyy) ", 
        default=f"{dt.now().strftime('%d.%m.%Y')}"
        )
    """ 
    def process_response(self, value):
        result_dt = None
        try:
            result_dt = dt.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise InvalidResponse(
                "Please enter a valid date fommat(dd.mm.yyyy)")

        if result_dt > dt.now():
            raise InvalidResponse(
                f"The date:{value} in the future - information not present")

        if result_dt < dt.strptime("02.09.1996", "%d.%m.%Y"):
            raise InvalidResponse(
                f"The date:{value} is too late - information presents "
                f"from 02.09.1996")

        return result_dt.strftime('%d.%m.%Y')

    def on_validate_error(self, value, error):
        # print(dir(error))
        console.print(f"Value: {value} is wrong. {error.message}", style="red")


if __name__ == "__main__":
    date_inp = DatePromptCurrency.ask(
        "Enter date begin:(dd.mm.yyyy) ", 
        default=f"{dt.now().strftime('%d.%m.%Y')}"
        )
    print(f"{date_inp=}")
