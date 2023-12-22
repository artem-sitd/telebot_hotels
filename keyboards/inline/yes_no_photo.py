from telebot import types

keyboard_yes_no = types.InlineKeyboardMarkup()
yes_button = types.InlineKeyboardButton(text="Да", callback_data="yes_button")
no_button2 = types.InlineKeyboardButton(text="Нет", callback_data="no_button2")
keyboard_yes_no.add(yes_button)
keyboard_yes_no.add(no_button2)
