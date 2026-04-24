from telebot.types import Message
from loader import bot
from keyboards.reply import main_menu


@bot.message_handler(func=lambda message: bot.get_state(message.from_user.id,
                                                        message.chat.id) is None)
def bot_echo(message: Message) -> None:
    state = bot.get_state(message.from_user.id, message.chat.id)
    print(f'DEBUG echo: текст={message.text}, состояние={state}')
    if state is None:
        bot.reply_to(message,
                     '🤷 Не понимаю тебя. Выбери одну из опций ниже.',
                     reply_markup=main_menu())