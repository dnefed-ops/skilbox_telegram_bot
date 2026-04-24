from telebot.types import Message
from loader import bot
from states import FlightsStates
from api.flights import search_flights
from keyboards.reply import main_menu


def start_flight_dialog(message: Message) -> None:
    """Запуск диалога подбора билета."""
    bot.set_state(message.from_user.id, FlightsStates.waiting_for_origin,
                  message.chat.id)
    bot.reply_to(
        message,
        '✈️ Введите IATA-код города вылета (аэропорта например: MOW, KJA, LED):'
    )


@bot.message_handler(func=lambda m: m.text == '✈️ Билет на самолёт')
def menu_flights(message: Message) -> None:
    """Обработчик кнопки из главного меню."""
    start_flight_dialog(message)


@bot.message_handler(func=lambda m: bot.get_state(m.from_user.id, m.chat.id) ==
                                    'FlightsStates:waiting_for_origin')
def process_origin(message: Message) -> None:
    origin = message.text.strip().upper()

    if len(origin) != 3 or not origin.isalpha():
        bot.reply_to(
            message,
            '❌ IATA-код должен состоять из 3 латинских букв (например: MOW, KJA). '
            'Попробуйте ещё раз:'
        )
        return
    bot.set_state(message.from_user.id, FlightsStates.waiting_for_destination,
                  message.chat.id)
    bot.reply_to(
        message,
        '✈️ Теперь введите IATA-код города назначения (например: MOW, KJA, LED):'
    )
    # Сохраним origin во встроенном хранилище состояний
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['origin'] = origin