import telebot
from module import Module
class SelfUsingModule (Module):

    def __init__(self, bot: telebot.TeleBot) -> None:
        super().__init__("Ручное управление", "самостоятельное написание в чаты, в которых находится бот", self.__call__, bot)

    def __call__(self, *args: any, **kwds: any) -> None:
        print("Это ручной вывод бота, все ваши сообщения будут написаны от имени бота. Введите id")

        chat_id = input()

        if (chat_id == "/exit"):
            return
        
        try:
            chat_id = int(chat_id)
        except ValueError:
            print("Id - число")
            return

        print("Все ваши сообщения кроме /exit будут выведены в чат:")
        input_string = input()
        while (input_string != "/exit"):
            self.bot.send_message(chat_id, input_string)
            input_string = input()
