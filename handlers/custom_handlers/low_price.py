from keyboards.inline.calendar import MyCalendar
from keyboards.inline.yes_no_photo import keyboard_yes_no
from loader import bot
from states.lowprice_state import LowePriceState as lp
from telebot.types import Message
from telebot import types
from RAPIDAPI.lowprice import check_city as cc
from RAPIDAPI.lowprice import get_lists as gl
from RAPIDAPI.lowprice import get_detail as gt
from time import sleep

# Локализация для календаря
LSTEP = {"y": "год", "m": "месяц", "d": "день"}


# Первое вхождение в команду /lowprice
@bot.message_handler(commands=["lowprice"])
def low_price(m: Message):
    bot.set_state(m.from_user.id, lp.city, m.chat.id)
    bot.send_message(
        m.from_user.id,
        f"1/6 Привет, {m.from_user.username} введите желаемый город "
        f"для поиска самых дешевых отелей",
    )


# Сохранение города, переход в состояние checkin
@bot.message_handler(state=lp.city)
def get_city(m: Message):
    if m.text.isalpha():
        check_city = cc(m.text)
        if check_city:
            with bot.retrieve_data(m.from_user.id, m.chat.id) as data:
                data["city"] = check_city
            bot.send_message(
                m.from_user.id,
                f"2/6 Выбранный город > {m.text} <, теперь необходимо "
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


# Сохранение даты заезда
@bot.callback_query_handler(func=MyCalendar.func(calendar_id=1))
def cal_checkin(c: types.CallbackQuery):
    result, key, step = MyCalendar(calendar_id=1).process(c.data)
    if not result and key:
        bot.edit_message_text(
            f"Выберите {LSTEP[step]} заезда",
            c.message.chat.id,
            c.message.message_id,
            reply_markup=key,
        )
    elif result:
        bot.set_state(c.from_user.id, lp.date_from_to, c.message.chat.id)
        with bot.retrieve_data(c.from_user.id, c.message.chat.id) as data:
            data["checkin"] = result  # Записывается дата заезда
            bot.send_message(c.from_user.id, f"Вы выбрали дату заезда {result}")
        date_from_to(
            c.message
        )  # Просто вызываем второй календарь (ниже) с датой выезда


@bot.message_handler(state=lp.date_from_to)
def date_from_to(m: Message):
    bot.send_message(m.chat.id, f"3/6 Теперь необходимо выбрать дату выезда")
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
        bot.set_state(c.from_user.id, lp.count_hotels, c.message.chat.id)
        with bot.retrieve_data(c.from_user.id, c.message.chat.id) as data:
            data["checkout"] = result  # Записывается дата выезда
            bot.send_message(c.from_user.id, f"Вы выбрали дату выезда {result}")
        bot.send_message(
            c.from_user.id,
            f"4/6 Теперь необходимо выбрать количество отелей (максимум 10)",
        )


@bot.message_handler(state=lp.count_hotels)
def get_count_hotels(m: Message):
    if not m.text.isdigit():
        bot.send_message(m.from_user.id, "Необходимо указать число")
    elif int(m.text) not in range(1, 11):
        bot.send_message(m.from_user.id, "Необходимо указать число от 1 до 10")
    else:
        with bot.retrieve_data(m.from_user.id, m.chat.id) as data:
            data["count_hotels"] = int(m.text)
            bot.send_message(m.from_user.id, f"{m.text} отелей будет показано")
        bot.send_message(
            m.from_user.id,
            f"5/6 Нужны ли будут фото отелей?",
            reply_markup=keyboard_yes_no,
        )


@bot.callback_query_handler(func=lambda c: c.data)
def get_answer_photo(call: types.CallbackQuery):
    if call.data == "yes_button":
        bot.set_state(call.from_user.id, lp.image_count, call.message.chat.id)
        bot.send_message(
            call.from_user.id,
            "Укажите количество фотографий (от 1 до 10)",
        )
    else:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data["image_count"] = None
        bot.set_state(call.from_user.id, lp.finish, call.message.chat.id)
        # Переходим к обработке всей информации


@bot.message_handler(state=lp.image_count)
def get_image_count(m: Message):
    if not m.text.isdigit():
        bot.send_message(m.chat.id, "Укажите число от 1 до 10")
    elif int(m.text) not in range(1, 11):
        bot.send_message(m.chat.id, "Укажите число от 1 до 10")
    else:
        bot.set_state(m.from_user.id, lp.finish, m.chat.id)
        with bot.retrieve_data(m.from_user.id, m.chat.id) as data:
            data["image_count"] = int(m.text)
        # Переходим к обработке всей информации


@bot.message_handler(state=lp.finish)
def finish(m: Message):
    bot.send_message(m.from_user.id, "Спасибо за ответы, собираю информацию")
    bot.set_state(m.from_user.id, None, m.chat.id)

    with bot.retrieve_data(m.from_user.id, m.chat.id) as data:
        response_list = gl(
            data["city"],
            data["checkin"],
            data["checkout"],
            data["count_hotels"],
            count_photo=data['image_count'])

    if response_list:
        for hotel in response_list:
            # обработка фото наверно будет здесь
            text = ""

            for k, v in hotel.items():
                text += f"*{k}* : {v}\n"
            bot.send_message(m.from_user.id, text, parse_mode="Markdown")
            # сюда вставить фото
            sleep(0.5)
