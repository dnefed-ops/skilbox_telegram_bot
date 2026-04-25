from telebot.apihelper import answer_pre_checkout_query
from telebot.types import Message, ReplyKeyboardRemove
from states import WeatherStates
from loader import bot
from api.location import get_location
from api.weather import get_weather
from keyboards.reply.main_menu import main_menu
from database.config import db, User, Request


def start_weather_dialog(message: Message) -> None:
    """Общаяя функция запуска диалога - вызывается из команды и из кнопки."""
    bot.set_state(message.from_user.id, WeatherStates.waiting_for_city,
                  message.chat.id)
    state = bot.get_state(message.from_user.id, message.chat.id)
    print(f'DEBUG start_weather_dialog: user_id={message.from_user.id}, chat_id={message.chat.id}, состояние={state}')
    bot.reply_to(message, '🌍 Введите название города (например: Москва или London):')


@bot.message_handler(commands=['weather'])
def cmd_weather(message: Message) -> None:
    """Обработчик команды /weather - запрашивает у пользователя название города"""
    start_weather_dialog(message)

@bot.message_handler(func=lambda m: True, state='*')
def debug_any(message: Message) -> None:
    state = bot.get_state(message.from_user.id, message.chat.id)
    print(f'DEBUG любое сообщение: текст={message.text}, состояние={state}')
    

@bot.message_handler(func=lambda m: bot.get_state(m.from_user.id, m.chat.id) == 'WeatherStates:waiting_for_city')
def process_city(message: Message) -> None:
    """Обрабатывает введённый город и выдаёт погоду."""
    print(f'DEBUG: process_city вызван, город = {message.text}')
    bot.delete_state(message.from_user.id, message.chat.id)
    city = message.text.strip()
    
    bot.reply_to(message, f'🔍 Ищу погоду для {city}...')
    coordinates = get_location(city)

    if not coordinates:
        bot.reply_to(
            message,
            '❌ Город не найден. Попробуйте написать иначе (например: Москва, Moscow, Красноярск).'
        )
        bot.delete_state(message.from_user.id, message.chat.id)
        return
    
    lat, lon = coordinates
    weather = get_weather(lat, lon)

    if not weather:
        bot.reply_to(message, '❌ Не удалось получить данные о погоде. Попробуйте позже.')
        bot.delete_state(message.from_user.id, message.chat.id)
        return
    
    text = (
        f'🏙 <b>{city.capitalize()}</b>\n\n'
        f'{weather["description"]}\n'
        f'🌡 Температура: <b>{weather["temperature"]}°C</b>\n'
        f'💨 Ветер: <b>{weather["wind_speed"]} км/ч</b>'
    )
    bot.send_message(message.chat.id, text, parse_mode='HTML',
                     reply_markup=main_menu())
    bot.delete_state(message.from_user.id, message.chat.id)

    with db:
        user, _ = User.get_or_create(
            telegram_id=message.from_user.id,
            defaults={
                'name': message.from_user.first_name or '',
                'telegram_name': message.from_user.username or ''
            }
        )
        Request.create(
            user_id=user.id,
            request=city,
            answer_request=f'{weather["description"]}, {weather["temperature"]}°C,'
                           f'ветер {weather["wind_speed"]} км/ч'
        )

print(f'DEBUG weather.py загружен, хендлеры: {bot.message_handlers[-3:]}')