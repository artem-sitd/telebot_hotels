from telebot import types

# Кнопки фото отелей
keyboard_yes_no = types.InlineKeyboardMarkup()
yes_button = types.InlineKeyboardButton(text="Да", callback_data="yes_button")
no_button2 = types.InlineKeyboardButton(text="Нет", callback_data="no_button2")
keyboard_yes_no.add(yes_button)
keyboard_yes_no.add(no_button2)

#  Кнопки выбора сортировок (не реализовано)
keyboard_sort = types.InlineKeyboardMarkup()
price_sort_button = types.InlineKeyboardButton(text='По цене от самый дешевых', callback_data='price')
distance_sort_button = types.InlineKeyboardButton(text='По расстоянию от центра', callback_data='distance')
keyboard_sort.add(price_sort_button)
keyboard_sort.add((distance_sort_button))
