## Команды для бота:

- /help - выводит справку по доступным командам
- /lowprice - вывод самых дешёвых отелей в городе (сортировка по цене от дешевых к дорогим)
- /highprice- вывод самых дорогих отелей в городе (сортировка по цене от дорогих к дешевым)
- /history - вывод истории поиска отелей
- /bestdeal - вывод отелей, наиболее подходящих по цене и расположению от центра (сортировка по расстоянию от центра)

База данных - Используется ORM peewee (также прилагается)\
Телеграмм - telebot\
Чувствительные данные - dotenv\
Запуск бота из корневой директории по команде - `python main.py`\
.env.template необходимо заполнить  вашими токенами от вашего бота и от [RapidApi](https://rapidapi.com/ru/apidojo/api/hotels4/)

