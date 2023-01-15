import telebot
import threading
import pathlib
import csv
import time
import os
from module import Module

class CollectorModule (Module):
    __isModuleWork = False
    __buffer = {}
    __refresh_thread: threading.Thread

    __file = ""
    
    __MAX_SIZE_OF_BUFFER = 3
    __REFRESH_TIME_MINUTES = 10
    __TARGET_ID = os.environ["TARGET_ID"] # 0 if for all people
    __HEADER = ["Message id", "Requests", "Reply"]

    def __init__(self, bot: telebot.TeleBot) -> None:
        super().__init__("Сборщик", "собирает данные для датасета", self.__call__, bot)

    def __call__(self, **kwds: any) -> None:
        if (self.__isModuleWork):
            self.__turn_off()
        else:
            self.__turn_on(**kwds)

        self.__isModuleWork = not self.__isModuleWork

    def __turn_off(self) -> None:
        print("Отключение сборки данных...")
        self.__close_file()
        print("Бот больше не собирает данные")
        

    
    def __turn_on(self, **kwds: any) -> None:
        print("Включение сборки данных...")

        self.__open_file()

        @self.bot.message_handler(content_types=["text"])
        def get_text_message(msg):
            if (msg.chat.type == "private"):
                return
            self.__process_msg(msg)

        self.bot.stop_polling()

        thr = threading.Thread(target=self.bot.polling, args=(False, False, 0, 20, 20, None, None, True), daemon=kwds["isDaemon"])
        thr.start()

        self.__refresh_thread = threading.Thread(target=self.__refresh_file, daemon=kwds["isDaemon"])
        self.__refresh_thread.start()

        print("Данные собираются")

    def __close_file(self):
        self.__file.close()

    def __open_file(self):
        if (pathlib.Path("dataset.csv").exists()):
            self.__file = open("dataset.csv", "a")
        else:
            print("Файла нет!")
            self.__file = open("dataset.csv", "w")
            csv.writer(self.__file).writerow(self.__HEADER)

    def __refresh_file(self):
        while (True):
            time.sleep(self.__REFRESH_TIME_MINUTES*60)
            self.__close_file()
            self.__open_file()
            #print("Файл был обновлен!")

    def __process_msg(self, msg):
        if (self.__file.closed): 
            return

        if (self.__TARGET_ID == 0):  # TODO: add listening for all
            return

        if (msg.chat.id not in self.__buffer):
            self.__buffer[msg.chat.id] = []

        if (msg.from_user.id == int(self.__TARGET_ID)):
            csv.writer(self.__file).writerow([msg.message_id, self.__buffer[msg.chat.id], msg.text])
            self.__buffer[msg.chat.id].clear()
            return

        self.__buffer[msg.chat.id].append(msg.text)

        if (self.__buffer[msg.chat.id].__len__() > self.__MAX_SIZE_OF_BUFFER):
            self.__buffer[msg.chat.id].pop(0)
        