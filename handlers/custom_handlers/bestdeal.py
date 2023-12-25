from loader import bot
from states.all_state import AllState as AS
from telebot.types import Message


def check_float(num):
    try:
        float(num.replace(',', '.'))
    except ValueError:
        return False
    return True


@bot.message_handler(state=AS.distance)
def get_distance(m: Message):
    if check_float(m.text):
        bot.set_state(m.from_user.id, AS.min_price, m.chat.id)
        with bot.retrieve_data(m.from_user.id, m.chat.id) as data:
            data["distance"] = float(m.text.replace(',', '.'))
        bot.send_message(m.from_user.id, f"Принято {m.text} км, теперь необходимо указать минимальный бюджет "
                                         f"за 1 ночь в долларах (например 14)")
    else:
        bot.send_message(m.from_user.id,
                         f"Необходимо указать максимально допустимое расстояние от центра города до отеля в км *(например 3)*",
                         parse_mode="Markdown")


@bot.message_handler(state=AS.min_price)
def get_min_price(m: Message):
    if check_float(m.text):
        bot.set_state(m.from_user.id, AS.max_price, m.chat.id)
        with bot.retrieve_data(m.from_user.id, m.chat.id) as data:
            data["min_price"] = float(m.text.replace(',', '.'))
        bot.send_message(m.from_user.id,
                         f"Принято {m.text} $ за одну ночь, теперь необходимо указать *МАКСИМАЛЬНЫЙ* бюджет за 1 ночь в долларах (например 54)",
                         parse_mode="Markdown")
    else:
        bot.send_message(m.from_user.id,
                         f"Необходимо указать *МИНИМАЛЬНЫЙ* допустимый бюджет за одну ночь в отеле *(например 3)*",
                         parse_mode="Markdown")


@bot.message_handler(state=AS.max_price)
def get_max_price(m: Message):
    if check_float(m.text):
        with bot.retrieve_data(m.from_user.id, m.chat.id) as data:
            if float(m.text.replace(',', '.')) >= data['min_price']:
                bot.set_state(m.from_user.id, AS.city, m.chat.id)
                data["max_price"] = float(m.text.replace(',', '.'))
                bot.send_message(m.from_user.id,
                                 f"Принято {m.text} $ за одну ночь, теперь необходимо указать город (например London)",
                                 parse_mode="Markdown")
            else:
                bot.send_message(m.from_user.id,
                                 f"Ваш бюджет меньше указанного вами минимального")
    else:
        bot.send_message(m.from_user.id,
                         f"Необходимо указать *МАКСИМАЛЬНЫЙ* допустимый бюджет за одну ночь в отеле *(например 54)*",
                         parse_mode="Markdown")
