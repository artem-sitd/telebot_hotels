import telebot, requests, json
from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from telebot.storage import StateMemoryStorage

class User(StatesGroup):
    city=State()
    checkin=State()
    checkout=State()

state_storage = StateMemoryStorage()
bot = telebot.TeleBot('5642140510:AAFmk2k0UDk6-nqMAQCQY3w1vL98x_bJ4zU', state_storage=state_storage)

# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id,
                     'Команды, используемые в этом боте: /help, /lowprice, /bestdeal, /history, /highprice')

#Если введена кнопка /help
@bot.message_handler(commands=["help"])
def help(m, res=False):
    bot.send_message(m.chat.id,
                     'Помощь по командам бота:\n/lowprice - вывод самых дешёвых отелей в городе\n/highprice- вывод самых дорогих отелей в городе\n/history - вывод истории поиска отелей\n/bestdeal - вывод отелей, наиболее подходящих по цене и расположению от центра')

#Если введена кнопка /highprice
@bot.message_handler(commands=["highprice"])
def highprice(m, res=False):
    bot.send_message(m.chat.id, 'Раздел еще не доступен')

#Если введена кнопка /bestdeal
@bot.message_handler(commands=["bestdeal"])
def bestdeal(m, res=False):
    bot.send_message(m.chat.id, 'Раздел еще не доступен')

#Если введена кнопка /history
@bot.message_handler(commands=["history"])
def history(m, res=False):
    bot.send_message(m.chat.id, 'Раздел еще не доступен')

#Если введена команда /lowprice
@bot.message_handler(commands=['lowprice']) #Активация состояний по /lowprice
def city(message):
    bot.send_message(message.chat.id,'Введите город')
    bot.set_state(message.from_user.id, User.city, message.chat.id) #Состояние меняется на заполнение города

#Записывается город, далее должен открыться календарь
@bot.message_handler(state=User.city)
def city(message):
    bot.send_message(message.chat.id, 'Теперь необходимо выбрать дату заезда')
    bot.set_state(message.from_user.id, User.checkin, message.chat.id) #Меняется состояние на календарь (дата заезда, но календарь не открывается)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text #записывается город
    calendar, step = DetailedTelegramCalendar(calendar_id=1).build()
    bot.send_message(message.chat.id,
                     f"Выберите {LSTEP[step]}",
                     reply_markup=calendar)

#Обработчик первого календаря дата заезда
@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def cal(c):
    result, key, step = DetailedTelegramCalendar(calendar_id=1).process(c.data)
    if not result and key:
        bot.edit_message_text(f"Выберите {LSTEP[step]} заезда",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        bot.set_state(c.message.from_user.id, User.checkout, c.message.chat.id)
        with bot.retrieve_data(c.from_user.id, c.message.chat.id) as data:
            data['checkin'] = result #Записывается дата заезда
        checkout(c.message) #Просто вызываем второй календарь (ниже) с датой выезда

#Второй календарь - дата выезда
@bot.message_handler(state=User.checkout)
def checkout(message):
    bot.send_message(message.chat.id, 'Теперь необходимо выбрать дату выезда')
    calendar, step = DetailedTelegramCalendar(calendar_id=2).build()
    bot.send_message(message.chat.id,
                     f"Выберите {LSTEP[step]}",
                     reply_markup=calendar)

#Обработчик второго календаря
@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
def cal(c):
    result, key, step = DetailedTelegramCalendar(calendar_id=2).process(c.data)
    if not result and key:
        bot.edit_message_text(f"Выберите {LSTEP[step]} заезда",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        with bot.retrieve_data(c.from_user.id, c.message.chat.id) as data:
            data['checkout']=result #Записывается дата выезда

        #Далее перменные, хранящие в себе собранную инфу и передается далее в отдельную функцию для отправки в RAPIDAPI
        checkout=bot.retrieve_data(c.from_user.id, c.message.chat.id).data['checkout']
        checkin=bot.retrieve_data(c.from_user.id, c.message.chat.id).data['checkin']
        city=bot.retrieve_data(c.from_user.id, c.message.chat.id).data['city']
        user_info(c.message, checkin, checkout, city) #Просто вызов функции ниже

@bot.message_handler() #Не знаю нужен тут этот хендлер или нет
def user_info(message, checkin, checkout, city):
    text=hotels(dest_id(city), checkin, checkout) #Перменная, храняющая текст в виде названия отелей, стоимость проживаний, собранную из функций hotels и dest_id
    bot.send_message(message.chat.id, text) #отправляет в телеграм чат собранную инфу от RAPIDAPI

# Получение destination ID
def dest_id(city):
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query":city,"locale":"en_US","currency":"USD"}
    headers = {
        "X-RapidAPI-Key": "aedda95579msh4c285520c78d123p128fdajsn5373e406d117",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring).text
    j=json.loads(response)
    destinationId=j['suggestions'][0]['entities'][0]['destinationId']
    return destinationId

#Отправка города, дат заезда, выезда в RAPIDAPI
def hotels(dest, checkin, checkout):
  url = "https://hotels4.p.rapidapi.com/properties/list"
  querystring = {"destinationId": dest, "pageNumber": "1", "pageSize": "25", "checkIn": checkin,
                 "checkOut": checkout, "adults1": "2", "sortOrder": "PRICE",
                 "locale": "en_US", "currency": "USD"}
  headers = {
    "X-RapidAPI-Key": "aedda95579msh4c285520c78d123p128fdajsn5373e406d117",
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
  }
  response = requests.request("GET", url, headers=headers, params=querystring).text
  j = json.loads(response)
  text=''
  for k, i in enumerate(j['data']['body']['searchResults']['results']):
    text+= str(k+1)+ f' Отель: {i["name"]}\n' \
          f'https://hotels.com/ho{i["id"]}\n' \
          f'Цена за сутки: {i["ratePlan"]["price"]["current"]}\n' \
          f'Общая цена: {i["ratePlan"]["price"]["fullyBundledPricePerStay"].replace("&nbsp;","")}\n\n'
  return text

#Если введён привет - отвечает именем бота. Если другой текст - отправляет в /help
@bot.message_handler(content_types=["text"])
def handle_text(message):
    if 'привет' in message.text.lower():
        bot.send_message(message.chat.id,
                         f'Привет, я бот - {bot.get_me().username} финальный проект Python Basic. Автор - Ситдиков Артем Альбертович')
    else:
        bot.send_message(message.chat.id, 'Используй только команды в /help')

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
bot.polling(none_stop=True)