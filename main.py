from menu import Menu
import telebot
import os

def main():
    bot = create_bot()

    menu = Menu(bot)

    while (menu() != 0):
       pass

def create_bot() -> telebot.TeleBot:
    token = os.environ["NEUROZIPU_TOKEN"]
    return telebot.TeleBot(token)



main()