# task_2.py
# 2. [ ] Створити клас Matrix, який буде мати наступний функціонал:
#    - 1. __init__ - вводиться кількість стовпців і кількість рядків
#    - 2. fill() - заповнить створений масив числами - по порядку. Наприклад:
#      ```
#      +────+────+
#      | 1  | 2  |
#      +────+────+
#      | 3  | 4  |
#      +────+────+
#      | 5  | 6  |
#      +────+────+
#      ```
#    - 3. print_out() - виведе створений масив (якщо він ще не заповнений 
# даними - вивести нулі

#    - 4. transpose() - перевертає створений масив. 
# Тобто, якщо взяти попередню таблицю, результат буде
#      ```
#      +────+────+────+
#      | 1  | 3  | 5  |
#      +────+────+────+
#      | 2  | 4  | 6  |
#      +────+────+────+
#      ```
#    - P.S. Всякі там Пандас/Нампай не використовувати - тільки хардкор ;)
#    - P.P.S. Вивід не обов’язково оформлювати у вигляді таблиці - головне, 
# щоб було видно, що це окремі стовпці / рядки

class Matrix:
    """Робота з 2х мірним масивом"""
    def __init__(self, cols: int, rows: int):
        """ Ініціація пустого 2х мірного масива """
        self._arr = [[0 for _ in range(cols)] for _ in range(rows)]

    @property
    def arr(self):
        return self._arr 

    @arr.setter
    def arr(self, new_arr):
        self._arr = new_arr

    def __getitem__(self, item):
        if isinstance(item, tuple):
            n_row, n_col, *_ = item
            if n_row < 0 or n_row >= len(self._arr):
                raise IndexError("This matrix not have row #{item}")
            if n_col < 0 or n_col >= len(self._arr[0]):    
                raise IndexError("This matrix not have col #{item}")
            return self._arr[n_row][n_col]
        elif isinstance(item, int):
            return self._arr[item]
        raise IndexError("Wrong indexes need [row, col] or [int]")

    def __setitem__(self, item, value):
        if not isinstance(item, tuple):
            raise IndexError("Wrong indexes need [row, col]")
        n_row, n_col, *_ = item
        if n_row < 0 or n_row >= len(self._arr):
            raise IndexError("This matrix not have row #{item}")
        if n_col < 0 or n_col >= len(self._arr[0]):    
            raise IndexError("This matrix not have col #{item}")
        self._arr[n_row][n_col] = value

    def fill(self):
        """ Заповнення комірок послідовними значеннями """
        beg_num = 0
        for idx_row, row in enumerate(self._arr):
            for idx_col, _ in enumerate(row):
                beg_num += 1
                self._arr[idx_row][idx_col] = beg_num

    def print_out(self):
        """ Вивід матриці """
        s_row_sep = "---".join(("+" for _ in range(len(self._arr[0]) + 1)))
        for row in self._arr:
            print(s_row_sep)
            lst_row = []
            for item in row:
                lst_row.append(f"{item:3}")
            print("|" + "|".join(lst_row)+"|")
        print(s_row_sep)

    def transpose(self):
        """Поворот матриці де №рядка стає №колонки"""
        cnt_rows = len(self._arr)
        cnt_cols = len(self._arr[0])
        arr_temp = Matrix(cnt_rows, cnt_cols)

        for i_row, row in enumerate(self._arr):
            for i_col, _ in enumerate(row):
                arr_temp[i_col, i_row] = self[i_row, i_col]

        self._arr = arr_temp


if __name__ == "__main__":
    print("Matric(2, 3)")
    m1 = Matrix(2, 3)
    m1.fill()
    m1.print_out()

    print()
    print(f"m1[1, 1] == {m1[1, 1]}")
    print("m1[1, 1] = 100")
    m1[1, 1] = 100
    m1.print_out()

    print()
    print("Matric(3, 4)")
    m2 = Matrix(3, 4)
    m2.fill()
    m2.print_out()

    print()
    print("transpose m1:")
    m1.transpose()
    m1.print_out()

    print()
    print("transpose m2:")
    m2.transpose()
    m2.print_out()