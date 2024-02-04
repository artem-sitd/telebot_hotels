## Проект выполнялся в рамках дипломной работы 
### Простой телеграмм бот, выводящий перечень отелей по параметрам, указываемые пользователем в процессе взаимодействия с ботом
## Команды для бота:

- /help - выводит справку по доступным командам
- /lowprice - вывод самых дешёвых отелей в городе (сортировка по цене от дешевых к дорогим)
- /highprice- вывод самых дорогих отелей в городе (сортировка по цене от дорогих к дешевым)
- /history - вывод истории поиска отелей
- /bestdeal - вывод отелей, наиболее подходящих по цене и расположению от центра (сортировка по расстоянию от центра)

### Применяемые инструменты:
* База данных - Используется ORM peewee (также прилагается)
* Телеграмм - telebot
* Чувствительные данные - dotenv
* Запуск бота из Корневой директории по команде - `python main.py`
* .env.template необходимо заполнить вашими токенами от вашего бота и от [RapidApi](https://rapidapi.com/ru/apidojo/api/hotels4/)
* Календарь -`https://github.com/artembakhanov/python-telegram-bot-calendar/tree/master`
* Форматирование кода - black, isort
### Демонстрация работы бота:

[![Alt text](https://img.youtube.com/vi/VI7by1Fgn3g/0.jpg)](https://www.youtube.com/watch?v=VI7by1Fgn3g)

