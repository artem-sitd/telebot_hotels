import datetime
from time import sleep

from telebot.types import CallbackQuery, InputMediaPhoto, Message
from telegram_bot_calendar import DetailedTelegramCalendar

from database.models import History as HS
from keyboards.inline.calendar import MyCalendar
from keyboards.inline.yes_no_photo import keyboard_yes_no
from loader import bot
from RAPIDAPI.lowprice import process_data as PD
from RAPIDAPI.responses import check_city as cc
from states.all_state import AllState as AS

from .fast_message import FastMessage as FM

# Локализация для календаря
LSTEP = {"y": "год", "m": "месяц", "d": "день"}


# Вхождение в команды /lowprice, /highprice, /bestdeal
@bot.message_handler(commands=["lowprice", "highprice", "bestdeal"])
def low_price(m: Message):
    bot.set_state(m.from_user.id, AS.city, m.chat.id)
    if m.text == "/lowprice":
        FM.low(m.from_user.id, m.from_user.username)
    if m.text == "/highprice":
        FM.high(m.from_user.id, m.from_user.username)
        with bot.retrieve_data(m.from_user.id, m.chat.id) as data:
            data["sort_by"] = -1
    if m.text == "/bestdeal":
        bot.set_state(m.from_user.id, AS.distance, m.chat.id)
        FM.best(m.from_user.id, m.from_user.username)
        with bot.retrieve_data(m.from_user.id, m.chat.id) as data:
            data["bestdeal"] = True


# Сохранение города, переход в состояние checkin
@bot.message_handler(state=AS.city)
def get_city(m: Message):
    if m.text.isalpha():
        check_city = cc(m.text)
        if check_city:
            with bot.retrieve_data(m.from_user.id, m.chat.id) as data:
                data["city"] = check_city
            bot.send_message(
                m.from_user.id,
                f"Выбранный город > {m.text} <, теперь необходимо "
                f"выбрать дату заезда",
            )
            calendar, step = MyCalendar(calendar_id=1).build()
            bot.send_message(
                m.from_user.id, f"Выберите {LSTEP[step]}", reply_markup=calendar
            )
        else:
            bot.send_message(m.from_user.id, "Необходимо ввести корректный город")
    else:
        bot.send_message(m.from_user.id, "Необходимо ввести корректный город")


temp = {}


# Сохранение даты заезда
@bot.callback_query_handler(func=MyCalendar.func(calendar_id=1))
def cal_checkin(c: CallbackQuery):
    result, key, step = MyCalendar(calendar_id=1).process(c.data)
    if not result and key:
        bot.edit_message_text(
            f"Выберите {LSTEP[step]} заезда",
            c.message.chat.id,
            c.message.message_id,
            reply_markup=key,
        )
    elif result:
        bot.set_state(c.from_user.id, AS.date_from_to, c.message.chat.id)
        with bot.retrieve_data(c.from_user.id, c.message.chat.id) as data:
            data["checkin"] = result  # Записывается дата заезда
            temp["checkin"] = result
            bot.send_message(c.from_user.id, f"Вы выбрали дату заезда {result}")
        date_from_to(
            c.message
        )  # Просто вызываем второй календарь (ниже) с датой выезда


@bot.message_handler(state=AS.date_from_to)
def date_from_to(m: Message):
    bot.send_message(m.chat.id, f"Теперь необходимо выбрать дату выезда")
    calendar, step = MyCalendar(calendar_id=2).build()
    bot.send_message(m.chat.id, f"Выберите {LSTEP[step]}", reply_markup=calendar)


# Обработчик второго календаря
@bot.callback_query_handler(func=MyCalendar.func(calendar_id=2))
def cal_checkout(c):
    result, key, step = MyCalendar(calendar_id=2).process(c.data)
    if not result and key:
        bot.edit_message_text(
            f"Выберите {LSTEP[step]} выезда",
            c.message.chat.id,
            c.message.message_id,
            reply_markup=key,
        )

    elif result:
        if temp["checkin"] <= result:
            bot.set_state(c.from_user.id, AS.count_hotels, c.message.chat.id)
            with bot.retrieve_data(c.from_user.id, c.message.chat.id) as data:
                data["checkout"] = result  # Записывается дата выезда
                bot.send_message(c.from_user.id, f"Вы выбрали дату выезда {result}")
            bot.send_message(
                c.from_user.id,
                f"Теперь необходимо выбрать количество отелей (максимум 10)",
            )
        else:
            bot.send_message(
                c.from_user.id, f"Дата выезда должна быть не раньше заезда"
            )


@bot.message_handler(state=AS.count_hotels)
def get_count_hotels(m: Message):
    if not m.text.isdigit() or int(m.text) not in range(1, 11):
        bot.send_message(m.from_user.id, "Необходимо указать число")
    else:
        with bot.retrieve_data(m.from_user.id, m.chat.id) as data:
            data["count_hotels"] = int(m.text)
            bot.send_message(m.from_user.id, f"{m.text} отелей будет показано")
        bot.send_message(
            m.from_user.id, f"Нужны ли будут фото отелей?", reply_markup=keyboard_yes_no
        )


# Не активируется AS.finish
@bot.callback_query_handler(func=lambda c: c.data)
def get_answer_photo(call: CallbackQuery):
    if call.data == "yes_button":
        bot.set_state(call.from_user.id, AS.image_count, call.message.chat.id)
        bot.send_message(
            call.from_user.id,
            "Укажите количество фотографий (от 1 до 10)",
        )
    else:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data["count_photo"] = None
        bot.set_state(call.from_user.id, AS.finish, call.message.chat.id)
        finish(call)  # ничего страшного, что подсвечивает, т.к. finish ожидает Message,
        # а здесь передается - CallbackQuery, но там потом проверка идет
        # Переходим к обработке всей информации


@bot.message_handler(state=AS.image_count)
def get_image_count(m: Message):
    if not m.text.isdigit() or int(m.text) not in range(1, 11):
        bot.send_message(m.chat.id, "Укажите число от 1 до 10")
    else:
        bot.set_state(m.from_user.id, AS.finish, m.chat.id)
        with bot.retrieve_data(m.from_user.id, m.chat.id) as data:
            data["count_photo"] = int(m.text)
        finish(m)  # Переходим к обработке всей информации


@bot.message_handler(state=AS.finish)
def finish(m: Message):
    chat_id = None

    # Проверка на Instance, т.к. если вызов этой функции происходит если пользователь отказался от фото,
    # тогда функция принимает CallbackQuery, вместо Message
    if isinstance(m, Message):
        chat_id = m.chat.id
    elif isinstance(m, CallbackQuery):
        chat_id = m.message.chat.id

    bot.send_message(chat_id, "Спасибо за ответы, собираю информацию")
    bot.set_state(m.from_user.id, None, chat_id)

    with bot.retrieve_data(m.from_user.id, chat_id) as data:
        response_list = PD(
            data["city"],
            data["checkin"],
            data["checkout"],
            data["count_hotels"],
            distance=data.get("distance"),
            bestdeal=data.get("bestdeal", False),
            min_price=data.get("min_price", 0),
            max_price=data.get("max_price", 1000),
            sort_by=data.get("sort_by", 1),
            count_photo=data["count_photo"],
        )

    if response_list:
        for hotel in response_list:
            text = ""
            medias = []
            for k, v in hotel.items():
                if k == "Название отеля":
                    HS.create(user_id=m.from_user.id, hotels=v)
                if k != "Фото":
                    text += f"*{k}* : {v}\n"
                if k == "Фото":
                    text += "*Фото*: 👇"
                    medias = [InputMediaPhoto(photo) for photo in v]
            bot.send_message(m.from_user.id, text, parse_mode="Markdown")
            sleep(0.1)
            if medias:
                bot.send_media_group(chat_id, medias)
            sleep(0.3)
