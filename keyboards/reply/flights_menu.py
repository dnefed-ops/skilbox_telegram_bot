from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def flights_sort_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(
        KeyboardButton('🔻 Самые дешёвые'),
        KeyboardButton('🔺 Самые дорогие')
    )
    return keyboard