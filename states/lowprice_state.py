from telebot.handler_backends import State, StatesGroup


class LowePriceState(StatesGroup):
    city = State()
    date_from_to = State()
    count_hotels = State()
    image = State()
    image_count = State()
    finish = State()
