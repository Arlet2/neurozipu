import telebot
import threading
import pathlib
import csv
import time
from module import Module

class CollectorModule (Module):
    __isModuleWork = False
    __buffer = []
    __refresh_thread: threading.Thread

    __file = ""
    
    __MAX_SIZE_OF_BUFFER = 5
    __MAN_X = 5029071602 # 0 if for all people
    __HEADER = ["Message id", "Requests", "Reply"]

    def __init__(self, bot: telebot.TeleBot) -> None:
        super().__init__("Сборщик", "собирает данные для датасета", self.__call__, bot)

    def __call__(self, *args: any, **kwds: any) -> None:
        if (self.__isModuleWork):
            self.__turn_off()
        else:
            self.__turn_on()

        self.__isModuleWork = not self.__isModuleWork

    def __turn_off(self) -> None:
        print("Отключение сборки данных...")
        self.__close_file()
        

    
    def __turn_on(self) -> None:
        print("Включение сборки данных...")

        self.__open_file()

        @self.bot.message_handler()
        def get_text_message(msg):
            self.__process_msg(msg)

        self.bot.stop_polling()

        thr = threading.Thread(target=self.bot.polling, args=(False, False, 0, 20, 20, None, None, True), daemon=True)
        thr.start()

        self.__refresh_thread = threading.Thread(target=self.__refresh_file, daemon=True)
        self.__refresh_thread.start()

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
            time.sleep(30)
            self.__close_file()
            self.__open_file()
            #print("Файл был обновлен!")

    def __process_msg(self, msg):
        if (self.__file.closed): # TODO: add listening for all
            return

        if(self.__MAN_X == 0):
            return

        if (msg.from_user.id == self.__MAN_X):
            csv.writer(self.__file).writerow([msg.message_id, self.__buffer, msg.text])
            self.__buffer.clear()
            return

        self.__buffer.append(msg.text)

        if (self.__buffer.__len__() > self.__MAX_SIZE_OF_BUFFER):
            self.__buffer.pop(0)
        