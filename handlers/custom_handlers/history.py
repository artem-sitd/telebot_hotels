from loader import bot
from telebot.types import Message, CallbackQuery
from database.models import History as HS
from time import sleep


@bot.message_handler(commands=["history"])
def get_history(m: Message):
    sleep(0.4)
    history = HS.select(HS.hotels).where(HS.user_id == m.from_user.id).dicts().execute()
    bot.send_message(m.from_user.id, "Ваш список запрошенных отелей:")
    bot.send_message(m.from_user.id, "\n".join(i["hotels"] for i in history))
