# task_4.py
#  Створіть клас, який буде повністю копіювати поведінку list, 
# за виключенням того, що індекси в ньому мають починатися з 1, 
# а індекс 0 має викидати помилку 
# (такого ж типу, яку кидає list якщо звернутися до неіснуючого індексу) 

# dir(list) : ['__class__', '__contains__', '__delattr__', 
# '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', 
# '__getattribute__', '__gt__', '__hash__', 
# '__iadd__', '__imul__', '__init_subclass__', '', 
# '__le__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', 
# '__reduce_ex__', '__reversed__', '__rmul__', '__setattr__', 
# '__sizeof__', '__subclasshook__', 

# realised:
# '__init__', '__repr__', '__str__', '__len__', '__setitem__', '__getitem__', 
# 'append', 'clear', 'copy','extend', 'count', 'index', 'insert', 'pop', 
# 'remove', 'sort', 'reverse', __iter__, __add__
# 


from collections.abc import Iterable


class MyListSimple:
    """ Проста інплементація сласу list на основі list із модифікацією
     поведінки """ 
    def __init__(self, *args):
        self._seq = []
        if len(args) == 0:
            return
        elif len(args) == 1:
            if isinstance(args[0], Iterable):
                self._seq.extend(args[0])
            else:
                self._seq.append(args[0])
        else:
            self._seq.extend(args)

    def __repr__(self):
        return f"MyList({','.join(self.str_seq)})"

    def __str__(self):
        return f"({','.join(self.str_seq)}) length:{len(self._seq)}"

    @property
    def str_seq(self):
        """ Допоміжна властивість для роботи __repr__ чи __str__ """
        return map(str, self._seq)

    def __len__(self):
        return len(self._seq)

    def __getitem__(self, item):
        if isinstance(item, int):
            if item == 0:
                raise IndexError("list index out of range")
            if item > 0:
                idx = item - 1
            else:
                idx = item
            return self._seq[idx]
        elif isinstance(item, slice):
            start, end, step = item.start, item.stop, item.step
            if start is None:
                start = 1
            if end is None:
                end = len(self._seq)
            if step is None:
                step = 1
            
            if start > 0:
                start -= 1
            if end > 0:                
                end -= 1

            return self._seq[start: end: step]
        return []

    def __setitem__(self, item, value):
        if isinstance(item, int):
            if item == 0:
                raise IndexError("list index out of range")
            self._seq[item - 1] = value

    def append(self, item):
        self._seq.append(item)

    def clear(self):
        self._seq.clear()

    def copy(self):
        return MyListSimple(self._seq.copy())

    def extend(self, seq):
        print(f"extend:{seq} {isinstance(seq, Iterable)} {type(seq)}")
        if isinstance(seq, Iterable):
            self._seq.extend(seq)

    def count(self, item):
        return sum(1 for _ in filter(lambda el: el == item, self._seq))

    def index(self, item):
        for idx, el in enumerate(self._seq):
            if el == item:
                return idx + 1
        raise ValueError(f"{item} is not in list")

    def insert(self, idx, item):
        if idx == 0 or idx > len(self._seq):
            raise IndexError("list index out of range")
        self._seq.insert(idx - 1, item)

    def pop(self, idx):
        if idx == 0 or idx > len(self._seq):
            raise IndexError("list index out of range")
        return self._seq.pop(idx - 1)        

    def remove(self, item):
        idx = self.index(item)
        self.pop(idx)

    def sort(self, key=None, reverse=False):
        """Sort the list in ascending order and return None."""
        self._seq.sort(key=key, reverse=reverse)

    def reverse(self):
        self._seq.reverse()

    def __iter__(self):
        return iter(self._seq)

    def __add__(self, other):
        print(other)
        result = self.copy()
        print(f"__add__{result=}")
        result.extend(other)
        print(f"__add__{result=}")
        return result


if __name__ == "__main__":
    print("Test variants constructor:")
    print("Create Empty:")
    lst1 = MyListSimple()
    print(f"{lst1=}")

    print()
    print("Create 1 not iterable item:")
    lst2 = MyListSimple(1)
    print(f"{lst2=}")

    print()
    print("Create many items:")
    lst3 = MyListSimple(1, 2, 3, 4)
    print(f"{lst3=}")

    print()
    print("Create many items with iterable:")
    lst4 = MyListSimple((1, 2, 3, "baz"), 4, 5, ["bar", "boo"], 6)
    print(f"{lst4=}")

    print()
    print("Create first one iterable:")
    lst5 = MyListSimple((1, 2, 3, "baz"))
    print(f"{lst5=}")

    lst6 = MyListSimple(range(15))
    print(f"{lst6=}")

    print()
    print()
    print("Test properties:")
    print("Test len():")    
    print(f"{len(lst1)=}")
    print()
    print(f"{len(lst4)=}")
    print()

    print("Test getitem:")
    print(f"lst5[2] == 2, get:{lst5[2]=}")
    print()
    print(f"lst4[2:4] == [4, 5], get:{lst4[2:4]=}")
    print()
    print(f"lst4[::2] == [4, ['bar', 'boo']], get:{lst4[::2]=}")

    print()
    print(f"lst6[-1] == 2, get:{lst6[-1]=}")
    print()
    print(f"lst6[-4:-1] == [11, 12, 13], get:{lst6[-4:-1]=}")
    print()
    print(f"lst6[-4:] == [11, 12, 13], get:{lst6[-4:]=}")
    print()
    print(f"lst6[1::3] == [0, 3, 6, 9, 12], get:{lst6[1::3]=}")
    print()

    print("Test __setitem__:")
    print(f"{lst5=}")
    print('lst5[1] = "Busu"')
    lst5[1] = "Busu"
    print(f"{lst5=}")
    print('lst5[1:3] = "Busu" not work')
    lst5[1:3] = "Busu"
    print(f"{lst5=}")
    print()

    print("Test append:")
    print(f"{lst5=}")
    print('lst5.append([134, 154])')
    lst5.append([134, 154])
    print(f"{lst5=}")
    print()

    print("Test clear:")
    print(f"{lst2=}")
    lst2.clear()    
    print(f"{lst2=}")
    print()

    print("Test copy:")
    print(f"{lst3=}")
    lst3_copy = lst3.copy()
    print("lst3_copy[2] = 400")
    lst3_copy[2] = 400
    print(f"{lst3=}")
    print(f"{lst3_copy=}")
    print()

    print("Test extend:")
    print(f"{lst3=}")
    print("lst3.extend([17, 18, 20])")
    lst3.extend([17, 18, 20])
    print(f"{lst3=}")
    print()

    print("Test count:")
    print(f"{lst3=}")
    print(f"{lst3.count(20)=}")
    print(f"{lst3.count(8)=}")
    lst3.extend([17, 18, 20])
    print(f"{lst3=}")
    print(f"{lst3.count(20)=}")
    print(f"{lst3.count(8)=}")
    print()

    print("Test index:")
    print(f"{lst3=}")
    print(f"{lst3.index(20)=}")
    try:
        print(f"{lst3.index(8)=}")
    except ValueError as ex:
        print("ValueError: ", ex)
    print()

    print("Test insert:")
    print(f"{lst3=}")
    print("lst3.insert(4, 25)")
    lst3.insert(4, 25)
    print(f"{lst3=}")
    print()

    print("Test pop:")
    print(f"{lst3=}")
    print("lst3.pop(6)")
    poped_val = lst3.pop(6)
    print(f"{lst3=}, {poped_val=}")
    print()
    
    print("Test remove:")
    print(f"{lst3=}")
    print("lst3.remove(17)")
    lst3.remove(17)
    print(f"{lst3=}")
    print()

    print("Test sort:")
    print(f"{lst3=}")
    print("lst3.sort()")
    lst3.sort()
    print(f"{lst3=}")
    print("lst3.sort(reverse=True)")
    lst3.sort(reverse=True)
    print(f"{lst3=}")
    print("lst3.sort(key=str)")
    lst3.sort(key=str)
    print(f"{lst3=}")
    print()

    print("Test reverse:")
    print(f"{lst3=}")
    print("lst3.reverse()")
    lst3.reverse()
    print(f"{lst3=}")
    print()

    print("Test __add__:")
    print(f"{lst3=}")
    print(f"{lst4=}")
    print(f"lst3 + lst4={lst3 + lst4}")
    print()
