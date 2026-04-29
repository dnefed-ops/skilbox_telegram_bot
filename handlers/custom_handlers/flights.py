from telebot.types import Message
from loader import bot
from states import FlightsStates
from api.flights import search_flights
from keyboards.reply import main_menu, flights_menu, flights_sort_menu
from api.city_search import get_iata_code
from api.airlines import get_airline_name


def start_flight_dialog(message: Message) -> None:
    """Запуск диалога подбора билета."""
    bot.set_state(message.from_user.id, FlightsStates.waiting_for_origin,
                  message.chat.id)
    bot.reply_to(
        message,
        '✈️ Введите Город вылета или (IATA-код аэропорта например: MOW, KJA, LED):'
    )


@bot.message_handler(func=lambda m: m.text == '✈️ Билет на самолёт')
def menu_flights(message: Message) -> None:
    """Обработчик кнопки из главного меню."""
    start_flight_dialog(message)


@bot.message_handler(func=lambda m: bot.get_state(m.from_user.id, m.chat.id) ==
                                    'FlightsStates:waiting_for_origin')
def process_origin(message: Message) -> None:
    city = message.text.strip()
    iata = get_iata_code(city)
    if not iata:
        bot.send_message(
            message.chat.id,
            '❌ Город не найден, попробуй ещё раз'
        )
        return
    bot.send_message(
        message.chat.id,
        f'✅ {city} → код аэропорта: {iata}\nТеперь введите город прилёта:'
    )
    with bot.retrieve_data(message.from_user.id) as data:
        data['origin'] = iata
    bot.set_state(message.from_user.id, FlightsStates.waiting_for_destination,
                  message.chat.id)


@bot.message_handler(func=lambda m: bot.get_state(m.from_user.id, m.chat.id) ==
                     'FlightsStates:waiting_for_destination')
def process_destination(message: Message) -> None:
    city = message.text.strip()
    iata = get_iata_code(city)
    if not iata:
        bot.send_message(
            message.chat.id,
            '❌ Город не найден, попробуй ещё раз'
        )
        return

    with bot.retrieve_data(message.from_user.id) as data:
        data['destination'] = iata
    bot.send_message(
        message.chat.id,
        f'✅ {city} → код аэропорта: {iata}\n'
        f'📅 Введите дату вылета в формате ГГГГ-ММ-ДД (например: 2026-05-10):'
    )
    bot.set_state(message.from_user.id, FlightsStates.waiting_for_date,
                  message.chat.id)


@bot.message_handler(func=lambda m: bot.get_state(m.from_user.id, m.chat.id) ==
                     'FlightsStates:waiting_for_date')
def process_date(message: Message) -> None:
    depart_date = message.text.strip()

    if len(depart_date) != 10 or depart_date[4] != '-' or depart_date[7] != '-':
        bot.reply_to(
            message,
            '❌ Неверный формат даты. Нужно ГГГГ-ММ-ДД, например: 2026-05-10. Попробуйте ещё раз:'
        )
        return

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['depart_date'] = depart_date

    bot.set_state(message.from_user.id, FlightsStates.waiting_for_sort,
                  message.chat.id)
    bot.reply_to(
        message,
        '💰 Какие билеты показать?',
        reply_markup=flights_sort_menu()
    )


@bot.message_handler(func=lambda m: bot.get_state(m.from_user.id, m.chat.id) ==
                     'FlightsStates:waiting_for_sort')
def process_sort(message: Message) -> None:
    text = message.text.strip()

    if text == '🔻 Самые дешёвые':
        sort = 'cheap'
    elif text == '🔺 Самые дорогие':
        sort = 'expensive'
    else:
        bot.reply_to(
            message,
            '❌ Выберите один из вариантов ниже:',
            reply_markup=flights_sort_menu()
        )
        return

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        origin = data.get('origin')
        destination = data.get('destination')
        depart_date = data.get('depart_date')

    bot.reply_to(
        message,
        f'🔍 Ищу билеты {origin} → {destination} на {depart_date[:7]}...'
    )

    flights =  search_flights(origin, destination, depart_date, sort=sort)

    if not flights:
        bot.send_message(
            message.chat.id,
            '❌ Не удалось найти билеты. Попробуйте другой месяц или другие города.',
            reply_markup=main_menu()
        )
        bot.delete_state(message.from_user.id, message.chat.id)
        return

    label = '🔻 Самые дешёвые' if sort == 'cheap' else '🔺 Самые дорогие'
    lines = [f'✈️ <b>{label} билеты {origin} → {destination}:</b>\n']
    for i, f in enumerate(flights, 1):
        lines.append(
            f'{i}. 🧾 Цена: <b>{f["price"]} RUB</b>\n'
            f'   Авиакомпания: <b>{f["airline"]}</b>\n'
            f'   Вылет: {f["departure_at"]}\n'
            f'   Пересадок: {f["transfers"]}\n'
        )

    text = '\n'.join(lines)
    bot.send_message(message.chat.id, text, parse_mode='HTML',
                     reply_markup=main_menu())
    bot.delete_state(message.from_user.id, message.chat.id)