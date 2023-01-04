from module import Module
from self_using_module import SelfUsingModule

class Menu:
    modules = []

    def __init__(self) -> None:
        self.modules.append(SelfUsingModule())
        pass
    def __call__(self) -> None:
        count = self.modules.__len__()

        print("Добро пожаловать в меню! Всего %s %d %s" 
            % (
            get_correct_string_by_number(count, ["доступен", "доступно", "доступно"]),
            count, 
            get_correct_string_by_number(count, ["модуль", "модуля", "модулей"])))

def get_correct_string_by_number(count: int, attribute: list) -> str:
    n  = count % 100
    n1 = count % 10

    if (n > 10 and n < 20): # 11-19
        return attribute[2]

    if (n1 > 1 and n1 < 5): # 2-4
        return attribute[1]

    if (n1 == 1): # 1
        return attribute[0]

    return attribute[2] # 5-9 and others