from telebot.handler_backends import State,StatesGroup
class User(StatesGroup):
    city=State()
    checkin=State()
    checkout=State()
