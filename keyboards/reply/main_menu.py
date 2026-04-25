from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu() -> ReplyKeyboardMarkup:
    """Главное меню бота 4 кнопки."""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(
        KeyboardButton('🌤 Прогноз погоды'),
        KeyboardButton('✈️ Билет на самолёт')
    )
    keyboard.row(
        KeyboardButton('📋 История запросов'),
        KeyboardButton('❓ Помощь')
    )
    return keyboard