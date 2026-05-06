from telebot.types import Message
from loader import bot
from keyboards.reply import main_menu


@bot.message_handler(commands=['help'])
def bot_help(message: Message)-> None:
    _send_help(message)


@bot.message_handler(func=lambda m: m.text == '❓ Помощь')
def menu_help(message: Message) -> None:
    _send_help(message)



def _send_help(message: Message) -> None:
    bot.send_message(
        message.chat.id,
        '📖 <b>Справка по боту</b>\n\n'

        '🌤 <b>Прогноз погоды</b>\n'
        'Введи название города на русском или английском.\n'
        '<i>Примеры: Москва, Красноярск, Bangkok, New York</i>\n\n'

        '✈️ <b>Билеты на самолёт</b>\n'
        'Шаг 1 — введи город вылета\n'
        'Шаг 2 — введи город прилёта\n'
        'Шаг 3 — укажи дату в формате ГГГГ-ММ-ДД\n'
        'Шаг 4 — выбери сортировку (дешёвые/дорогие)\n'
        'Бот покажет 5 вариантов с ссылкой на покупку.\n'
        '<i>Примеры городов: Москва, Сочи, Пхукет, Дубай</i>\n\n'

        '📋 <b>История запросов</b>\n'
        'Хранит последние 5 запросов погоды и билетов.\n\n'

        '⚠️ <b>Важно знать</b>\n'
        '— Цены на билеты ориентировочные, актуальная стоимость на сайте\n'
        '— Дата вылета: только будущие даты\n'
        '— Если город не найден — попробуй написать иначе\n\n'

        '🆘 <b>Команды</b>\n'
        '/start — перезапустить бота\n'
        '/help — показать эту справку\n\n'

        'По всем вопросам: @dnefed_tg',
        parse_mode='HTML',
        reply_markup=main_menu()
    )