from module import Module
import telebot
import threading

class DefaultModule (Module):
    def __init__(self, bot: telebot.TeleBot) -> None:
        super().__init__("Стандартный модуль", "работает по умолчанию", self.__call__, bot)

    def __call__(self, *args: any, **kwds: any) -> None:
        @self.bot.message_handler()
        def get_text_message(msg):
            if(msg.text == "/id"):
                self.bot.send_message(msg.chat.id, msg.chat.id)
        
        #self.bot.polling(none_stop=True, interval=0)
        thr = threading.Thread(target=self.bot.polling, args=(False, False, 0, 20, 20, None, None, True), daemon=True)

        thr.start()