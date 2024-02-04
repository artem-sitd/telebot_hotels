from time import sleep

from telebot.types import CallbackQuery, Message

from database.models import History as HS
from loader import bot


@bot.message_handler(commands=["history"])
def get_history(m: Message):
    sleep(0.4)
    history = HS.select(HS.hotels).where(HS.user_id == m.from_user.id).dicts().execute()
    bot.send_message(m.from_user.id, "Ваш список запрошенных отелей:")
    bot.send_message(m.from_user.id, "\n".join(i["hotels"] for i in history))
