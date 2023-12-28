from loader import bot


class FastMessage:
    @classmethod
    def low(cls, id, name):
        bot.send_message(
            id,
            f"Привет, __{name}__ введите желаемый город для поиска самых *дешевых* отелей",
            parse_mode="MarkdownV2",
        )

    @classmethod
    def high(cls, id, name):
        bot.send_message(
            id,
            f"Привет, __{name}__ введите желаемый город для поиска самых *дорогих* отелей",
            parse_mode="MarkdownV2",
        )

    @classmethod
    def best(cls, id, name):
        bot.send_message(
            id,
            f"Привет, __{name}__ введите *максимальное расстояние до центра* города для поиска самых *выгодных* отелей",
            parse_mode="MarkdownV2",
        )
