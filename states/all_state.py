from telebot.handler_backends import State, StatesGroup


class AllState(StatesGroup):
    city = State()
    date_from_to = State()
    count_hotels = State()
    image = State()
    image_count = State()
    distance = State()  # bestdeal
    min_price = State()  # bestdeal
    max_price = State()  # bestdeal
    finish = State()
