from module import Module
import telebot
from self_using_module import SelfUsingModule
from collector_module import CollectorModule
from default_module import DefaultModule

class Menu:
    modules = []

    def __init__(self, bot: telebot.TeleBot) -> None:
        self.modules.append(SelfUsingModule(bot))
        self.modules.append(CollectorModule(bot))

        DefaultModule(bot)()

    def __call__(self) -> int:
        count = self.modules.__len__()

        print("Добро пожаловать в меню! Всего %s %d %s" 
            % (
            get_correct_string_by_number(count, ["доступен", "доступно", "доступно"]),
            count, 
            get_correct_string_by_number(count, ["модуль", "модуля", "модулей"])))

        print("Выберете один из доступных модулей:\n")

        print("0) Выход")

        for i in range(len(self.modules)):
            print(str(i+1)+") "+ self.modules[i].name + " - " + self.modules[i].description)

        print("Вы выбираете: ", end="")

        try:
            mode : int = int(input())
        except ValueError:
            print("Нужно ввести число. Сброс...")
            return

        mode-=1

        if (mode >= self.modules.__len__()):
            print("Введите корректный индекс для модуля")
            return

        if (mode == -1):
            print("Завершение программы...")
            return 0

        self.modules[mode]()

        

def get_correct_string_by_number(count: int, word_list: list) -> str:
    n  = count % 100
    n1 = count % 10

    if (n > 10 and n < 20): # 11-19
        return word_list[2]

    if (n1 > 1 and n1 < 5): # 2-4
        return word_list[1]

    if (n1 == 1): # 1
        return word_list[0]

    return word_list[2] # 5-9 and others