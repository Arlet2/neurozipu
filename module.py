import telebot
class Module:
    name: str
    description: str
    action = ()
    bot: telebot.TeleBot

    def __init__(self, name: str, description: str, action, bot: telebot.TeleBot) -> None:
        self.name = name
        self.description = description
        self.action = action
        self.bot = bot