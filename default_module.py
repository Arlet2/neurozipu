from module import Module
import telebot
import threading
import os
from menu import Menu

class DefaultModule (Module):

    __father_id = int(os.environ["FATHER_ID"])
    __menu : Menu

    def __init__(self, bot: telebot.TeleBot, menu: Menu) -> None:
        super().__init__("Стандартный модуль", "работает по умолчанию", self.__call__, bot)
        self.__menu = menu

    def __call__(self, *args: any, **kwds: any) -> None:
        @self.bot.message_handler(commands=["id"])
        def get_text_message(msg):
            print(msg)
            self.bot.send_message(msg.chat.id, msg.chat.id)

        @self.bot.message_handler(commands=["kill"])
        def get_text_message(msg):
            if(msg.from_user.id == self.__father_id):
                print("Отключение по запросу...")
                thr = threading.Thread(target=self.__menu.stop, daemon=True)
                thr.start()

        thr = threading.Thread(target=self.bot.polling, args=(False, False, 0, 20, 20, None, None, True), daemon=True)

        thr.start()