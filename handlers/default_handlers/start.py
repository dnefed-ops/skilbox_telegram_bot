from telebot.types import Message
from loader import bot
from keyboards.reply import main_menu


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    bot.reply_to(
        message,
        f'Привет, {message.from_user.full_name}! 👋\n\nВыбери что тебя интересует:',
        reply_markup=main_menu()
    )