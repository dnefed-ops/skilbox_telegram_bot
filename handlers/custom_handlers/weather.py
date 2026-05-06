from telebot.types import Message, ReplyKeyboardRemove
from states import WeatherStates
from loader import bot
from api.weather import get_weather, get_city_coordinates
from keyboards.reply.main_menu import main_menu
from database.config import db, User, Request


MENU_BUTTONS = {
    '🌤 Прогноз погоды',
    '✈️ Билет на самолёт',
    '❓ Помощь',
    '📋 История запросов'
}

def start_weather_dialog(message: Message) -> None:
    """Общаяя функция запуска диалога - вызывается из команды и из кнопки."""
    bot.set_state(message.from_user.id, WeatherStates.waiting_for_city,
                  message.chat.id)
    bot.reply_to(message, '🌍 Введите название города (например: Москва или London):')


@bot.message_handler(func=lambda m: m.text == '🌤 Прогноз погоды')
def menu_weather(message: Message) -> None:
    """Обработчик команды /weather - запрашивает у пользователя название города"""
    start_weather_dialog(message)


@bot.message_handler(func=lambda m: bot.get_state(m.from_user.id, m.chat.id) == 'WeatherStates:waiting_for_city')
def process_city(message: Message) -> None:
    city = message.text.strip()

    if city in MENU_BUTTONS:
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.process_new_messages([message])
        return

    bot.send_message(message.chat.id, f'🔍 Ищу погоду для {city}...')

    # ✅ Сначала геокодинг — город реально существует?
    location = get_city_coordinates(city)
    if not location:
        bot.send_message(
            message.chat.id,
            '❌ Город не найден. Попробуйте написать иначе (например: Москва, Moscow).'
        )
        return

    weather = get_weather(location['lat'], location['lon'])
    if not weather:
        bot.send_message(message.chat.id, '❌ Не удалось получить погоду. Попробуйте позже.')
        return

    user = User.get_or_none(User.telegram_id == message.from_user.id)
    if user:
        Request.create(
            user_id=user.id,
            request_type='weather',
            request=city,
            answer_request=(
                f'{location["name"]}, {location["country"]} | '
                f'{weather["icon"]} {weather["description"]} | '
                f'{round(weather["temperature"])}°C | '
                f'Ветер: {weather["wind_speed"]} км/ч'
            ),
        )

    bot.send_message(
        message.chat.id,
        f'🏙 {location["name"]}, {location["country"]}\n\n'
        f'{weather["icon"]} {weather["description"]}\n'
        f'🌡 Температура: {round(weather["temperature"])}°C\n'
        f'💨 Ветер: {weather["wind_speed"]} км/ч',
        reply_markup=main_menu()
    )
    bot.delete_state(message.from_user.id, message.chat.id)