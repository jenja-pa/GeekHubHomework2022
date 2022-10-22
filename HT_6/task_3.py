# task_3.py
# 3. На основі попередньої функції (скопіюйте кусок коду) створити наступний скрипт:
#    а) створити список із парами ім'я/пароль різноманітних видів (орієнтуйтесь по правилам своєї функції) - як валідні, так і ні;
#    б) створити цикл, який пройдеться по цьому циклу і, користуючись валідатором, перевірить ці дані 
# і надрукує для кожної пари значень відповідне повідомлення, наприклад:
#       Name: vasya
#       Password: wasd
#       Status: password must have at least one digit
#       -----
#       Name: vasya
#       Password: vasyapupkin2000
#       Status: OK
#    P.S. Не забудьте використати блок try/except ;)

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
    lst = [
        ("vasya", "wasd", "Password not contains digit"),
        ("vasya", "vasyapupkin2000", "Password not contains upper leter"),
        ("vasya", "vasyapuPKin2000", "All Ok"),


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
        ]

    for case in lst:
        try:
            validations(*case[:2])
        except NameIncorrectException as ex:
            print(f"Name: {case[0]}")
            print(f"Password: {case[1]}")
            print(f"Status: {ex}\n------")
        except PasswordIncorrectException as ex:
            print(f"Name: {case[0]}")
            print(f"Password: {case[1]}")
            print(f"Status: {ex}\n------")
        else:
            print(f"Name: {case[0]}")
            print(f"Password: {case[1]}")
            print(f"Status: Ok\n------")
