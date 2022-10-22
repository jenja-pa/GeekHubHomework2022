# task_2.py
# Створіть функцію для валідації пари ім'я/пароль за наступними правилами:
#    - ім'я повинно бути не меншим за 3 символа і не більшим за 50;
#    - пароль повинен бути не меншим за 8 символів і повинен мати хоча б одну
#    цифру;
#    - якесь власне додаткове правило :)
# Мої додаткові правила:
#    - пароль повинен містити тільки латинські літери числа та символ _
#    - пароль повинен містити хоча б одну Велику і малу літеру
#    - ім'я повинно містити тільки латиські літери цифри та символи: - і _
#    - ім'я не повинно починатись числом

#    Якщо якийсь із параметрів не відповідає вимогам - породити виключення із відповідним текстом.
class NameIncorrectException(Exception):
    pass
class PasswordIncorrectException(Exception):
    pass

def validations(name, pwd):
    digits = (*map(str, range(10)), )
    lower_lets = (*map(chr, (el for el in range(ord('a'), ord("z")+1))), )
    upper_lets = (*map(chr, (el for el in range(ord('A'), ord("Z")+1))), )
    service_name_chars = ("_", "-")
    service_pwd_chars = ("_", )

    valid_name_chars = (*digits, *lower_lets, *upper_lets, *service_name_chars)
    valid_pwd_chars = (*digits, *lower_lets, *upper_lets, *service_pwd_chars)

    if len(name) < 3:
        raise NameIncorrectException(f"Your name '{name}' is short")
    elif len(name) > 50:
        raise NameIncorrectException(f"Your name '{name}' is too long")
    elif len(set(name) - set(valid_name_chars)) != 0:
        raise NameIncorrectException(f"Your name '{name}' contain incorrect symbols")
    elif name[0] in digits:
        raise NameIncorrectException(f"Your name '{name}' begins from incorrect symbols")

    if len(pwd) < 8:
        raise PasswordIncorrectException(f"Your password '{pwd}' is short")
    elif len(set(pwd) - set(digits)) == len(set(pwd)):
        raise PasswordIncorrectException(f"Your password '{pwd}' must contain least one digit")
    elif len(set(pwd) - set(valid_pwd_chars)) != 0:
        raise PasswordIncorrectException(f"Your password '{pwd}' contain incorrect symbols")
    elif len(set(pwd) - set(lower_lets)) == len(set(pwd)):
        raise PasswordIncorrectException(f"Your password '{pwd}' must contain least one char in lower registry")
    elif len(set(pwd) - set(upper_lets)) == len(set(pwd)):
        raise PasswordIncorrectException(f"Your password '{pwd}' must contain least one char in UPPER registry")


if __name__ == "__main__":
    i_test_crash_cases = (
        ("bo", "lkdfkj8UU9375_", "Short name"),
        ("bolkldjflksjljweurxwnyrwuie_ejkUYYRRRSD23948309284as______hx", "lkdfkj8UU9375_", "Long name"),
        ("bo%$()__hdfh", "lkdfkj8UU9375_", "Name contain incorect symbols"),
        ("2boo", "lkdfkj8UU9375_", "Name begins from digit"),        

        ("booBaz", "lkD3_", "Password too small"),
        ("booBaz", "lkцоUEdtd_", "Password not contains digit"),
        ("booBaz", "lkц4о%$^&U7Edtd_", "Password contains wrong symbol"),
        ("booBaz", "TWERV5U8_", "Password not contains lower leter"),
        ("booBaz", "rehhe5dfkjk45_djfh8", "Password not contains upper leter"),


        ("bo_oBaz", "lk45_UThd_", "All ok"),
        ("_cat_bignBaz", "_k884hfhDRElk45hd", "All ok"),
        )

    for case in i_test_crash_cases:
        try:
            validations(*case[:2])
        except NameIncorrectException as ex:
            print(f"Name Error: description:{case[2]}")
            print(f"reason: {ex}\n")
        except PasswordIncorrectException as ex:
            print(f"Password Error: description:{case[2]}")
            print(f"reason: {ex}\n")
        else:
            print(f"No Exception occured:{case[0]}:{case[1]} - {case[2]}")




