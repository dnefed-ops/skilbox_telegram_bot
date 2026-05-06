from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def history_menu() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton('🌤 История погоды'),
        KeyboardButton('✈️ История билетов'),
    )
    markup.add(KeyboardButton('🏠 Главное меню'))
    return markup