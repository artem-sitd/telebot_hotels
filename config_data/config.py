import os

from dotenv import find_dotenv, load_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
headers = {
    "X-RapidAPI-Key": RAPID_API_KEY,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
}
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("lowprice", "вывод самых дешёвых отелей в городе"),
    ("highprice", "вывод самых дорогих отелей в городе"),
    ("history", "вывод истории поиска отелей"),
    ("bestdeal", "вывод отелей, наиболее подходящих по цене и расположению от центра"),
)
