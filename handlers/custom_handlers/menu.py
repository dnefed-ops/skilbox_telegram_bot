from telebot.types import Message
from loader import bot
from keyboards.reply.main_menu import main_menu


@bot.message_handler(func=lambda m: m.text == '🌤 Прогноз погоды')
def menu_weather(message: Message) -> None:
    from handlers.custom_handlers.weather import start_weather_dialog
    print(f'DEBUG menu_weather вызван, chat_id={message.chat.id}, user_id={message.from_user.id}')
    start_weather_dialog(message)


@bot.message_handler(func=lambda m: m.text == '✈️ Билет на самолёт')
def menu_flights(message: Message) -> None:
    bot.reply_to(message,
                 '✈️ Команда /flights в разработке — скоро будет!. Выберите другую опцию.',
                 reply_markup=main_menu()
                 )


@bot.message_handler(func=lambda m: m.text == '❓ Помощь')
def menu_help(message: Message) -> None:
    from handlers.default_handlers.help import bot_help
    bot_help(message)