from telegram_bot_calendar import DetailedTelegramCalendar
import datetime


class MyCalendar(DetailedTelegramCalendar):
    def __init__(self, **kwargs):
        super().__init__(min_date=datetime.date.today(), locale="ru", **kwargs)
