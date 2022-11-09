from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from loader import bot


@bot.message_handler(commands=['help'])
def bot_help(m):
    bot.send_message(m.chat.id,
                     'Помощь по командам бота:\n/lowprice - вывод самых дешёвых отелей в городе\n'
                     '/highprice- вывод самых дорогих отелей в городе\n/history - вывод истории поиска отелей\n'
                     '/bestdeal - вывод отелей, наиболее подходящих по цене и расположению от центра')