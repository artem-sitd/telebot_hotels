from telebot.types import Message

from loader import bot

@bot.message_handler(commands=['start'])
def start(m, res=False):
    bot.send_message(m.chat.id,
                     f'Привет, {m.from_user.first_name}\n'
                     f'Команды, используемые в этом боте: /help, /lowprice, /bestdeal, /history, /highprice')

