# task_1.py
# [X] Створити клас Calc, який буде мати атребут last_result та 4 методи. 
# Методи повинні виконувати математичні операції з 2-ма числами, а саме 
# додавання, віднімання, множення, ділення.
#    - [X] Якщо під час створення екземпляру класу звернутися до атрибута 
# last_result він повинен повернути пусте значення.
#    - [X] Якщо використати один з методів - last_result повинен повернути 
# результат виконання ПОПЕРЕДНЬОГО методу.
#    ```
#    Example:
#     last_result --> None
#     1 + 1
#     last_result --> None
#     2 * 3
#     last_result --> 2
#     3 * 4
#     last_result --> 6
#     ...
#    ```
#    - [X] Додати документування в клас 

class Calc:
    """
    A class user to execute simple matematical operation with ability giving 
    result of preexecuted operation 

    ```
    Attributes
    ----------
    last_result : int
        result of last operation
    result : int
        result of current operatio

    Methods
    -------
    add(operand1, operand2):
        Put value of the atribute result into attribute last_result;
        Perform operation operand1 + operand2, and  put value of the result 
        operation into attribute result
    """
    def __init__(self):
        """
        Parameters
        ----------
        Empty
        """
        self.last_result = None
        self.result = None

    def add(self, operand1, operand2):
        """Perform operation +

        Perform operation + above two operends, and provide changes save result
        """        
        self.last_result = self.result
        self.result = operand1 + operand2

    def sub(self, operand1, operand2):        
        """Perform operation -

        Perform operation - above two operends, and provide changes save result
        """        
        self.last_result = self.result
        self.result = operand1 - operand2

    def mul(self, operand1, operand2):        
        """Perform operation *

        Perform operation * above two operends, and provide changes save result
        """        
        self.last_result = self.result
        self.result = operand1 * operand2

    def div(self, operand1, operand2):        
        """Perform operation /

        Perform operation / above two operends, and provide changes save result
        """        
        self.last_result = self.result
        self.result = operand1 / operand2


if __name__ == "__main__":
    # create obj, class Cals
    calc = Calc()
    # last_result --> None
    print(f"After creation. {calc.last_result=}, Expected result: None")
    #     1 + 1
    calc.add(1, 1)
    #     last_result --> None
    print(f"After    1 + 1. {calc.last_result=}, Expected result: None")
    #     2 * 3
    calc.mul(2, 3)
    #     last_result --> 2
    print(f"After    2 + 3. {calc.last_result=}, Expected result: 2")
    #     3 * 4
    calc.mul(3, 4)
    #     last_result --> 6
    print(f"After    3 * 4. {calc.last_result=}, Expected result: 6")
    #   12 / 3
    #   last_result --> 12
    calc.div(12, 3)
    print(f"After   12 / 3. {calc.last_result=}, Expected result: 12")
    #   17 - 2
    #   last_result --> 4
    calc.sub(17, 2)
    print(f"After   17 - 2. {calc.last_result=}, Expected result: 4")
