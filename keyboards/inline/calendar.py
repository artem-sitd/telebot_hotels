from telegram_bot_calendar import DetailedTelegramCalendar
import datetime


class MyCalendar(DetailedTelegramCalendar):
    def __init__(self, min_date=datetime.date.today(), **kwargs):
        super().__init__(min_date=min_date, locale="ru", **kwargs)

