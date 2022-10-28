# task_2.py
# 2. Написати функцію, яка приймає два параметри: 
    # ім'я (шлях) файлу та кількість символів. 

# Файл також додайте в репозиторій. 
# На екран має бути виведений список із трьома блоками - символи з початку, із середини та з кінця файлу. 
# Кількість символів в блоках - та, яка введена в другому параметрі. 
# Придумайте самі, як обробляти помилку, наприклад, коли кількість символів більша, 
#  ніж є в файлі або, наприклад, файл із двох символів і треба вивести по одному символу, 
#  то що виводити на місці середнього блоку символів?). 
# Не забудьте додати перевірку чи файл існує.
import  os.path

class FileTooShortError(Exception):
    pass


def boo(fname, cnt_chars):
    """
    Функція, що повериає три блоки символів довжиною cnt_chars із
    початку середини та кінця файла

    Вхідні дані:
     - ім'я файла
     - довжина блоку для виводу'

    Вихідні дані:
     - вивід на екран, хоча логічніше повертати отриманий список
    """
    if not os.path.exists(fname):
        raise FileExistsError(f"Your file: {fname} does not exsists")

    file_size = os.path.getsize(fname)
    if file_size < cnt_chars:
        raise FileTooShortError(f"Your file {fname} too short for execution function operation")

    lst = []
    with open(fname) as f:
        f.seek(0)
        lst.append(f.read(cnt_chars))

        midle_pos = (file_size // 2) - (cnt_chars // 2)
        f.seek(midle_pos)
        lst.append(f.read(cnt_chars))

        f.seek(file_size - cnt_chars)
        lst.append(f.read(cnt_chars))

    print(lst)
    return lst


if __name__ == "__main__":
    boo("test_1.txt", 1)    
    boo("test_1.txt", 3)
    boo("test_1.txt", 4)
    boo("test_1.txt", 7)
    # boo("test_1.txt", 15)
    boo("test_2.txt", 1)    

