# task_5.py
# 5. Напишіть функцію,яка приймає на вхід рядок та повертає кількість окремих 
# регістро-незалежних букв та цифр, які зустрічаються в рядку більше ніж 1 раз. 
# Рядок буде складатися лише з цифр та букв (великих і малих). 
# Реалізуйте обчислення за допомогою генератора в один рядок
#     Example (input string -> result):
#     "abcde" -> 0            # немає символів, що повторюються
#     "aabbcde" -> 2          # 'a' та 'b'
#     "aabBcde" -> 2          # 'a' присутнє двічі і 'b' двічі (`b` та `B`)
#     "indivisibility" -> 1   # 'i' присутнє 6 разів
#     "Indivisibilities" -> 2 # 'i' присутнє 7 разів та 's' двічі
#     "aA11" -> 2             # 'a' і '1'
#     "ABBA" -> 2             # 'A' і 'B' кожна двічі

def cnt_symbs(value):
    """
    Однорядкова функція підрахунку кількості регістро незалежних символів, що повторюються
    """
    return len([item for item in set(value.upper()) if value.upper().count(item) > 1])


if __name__ == "__main__":
    print(cnt_symbs("abcde"))   #-> 0            # немає символів, що повторюються
    print(cnt_symbs("aabbcde")) #-> 2          # 'a' та 'b'
    print(cnt_symbs("aabBcde")) # -> 2          # 'a' присутнє двічі і 'b' двічі (`b` та `B`)
    print(cnt_symbs("indivisibility")) # -> 1   # 'i' присутнє 6 разів
    print(cnt_symbs("Indivisibilities")) # -> 2 # 'i' присутнє 7 разів та 's' двічі
    print(cnt_symbs("aA11")) # -> 2             # 'a' і '1'
    print(cnt_symbs("ABBA")) # -> 2             # 'A' і 'B' кожна двічі
