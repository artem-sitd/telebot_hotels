import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('5642140510:AAFmk2k0UDk6-nqMAQCQY3w1vL98x_bJ4zU')
RAPID_API_KEY = os.getenv('aedda95579msh4c285520c78d123p128fdajsn5373e406d117')
DEFAULT_COMMANDS = (('start', "Запустить бота"), ('help', "Вывести справку"),
                    ('lowprice','вывод самых дешёвых отелей в городе'),
                        ('highprice','вывод самых дорогих отелей в городе'),
                       ('history','вывод истории поиска отелей'),
                    ('bestdeal','вывод отелей, наиболее подходящих по цене и расположению от центра'))