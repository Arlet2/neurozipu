from menu import Menu
import telebot
import os

def __main__():
    bot = create_bot()

    menu = Menu(bot)

    while (menu() != 0):
       pass

def create_bot() -> telebot.TeleBot:
    token = os.environ["NEUROZIPU_TOKEN"]
    return telebot.TeleBot(token)



__main__()