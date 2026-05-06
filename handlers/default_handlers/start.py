from telebot.types import Message
from loader import bot
from keyboards.reply import main_menu
from database.config import User


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    User.get_or_create(
        telegram_id=message.from_user.id,
        defaults={
            'name': message.from_user.full_name,
            'telegram_name': message.from_user.username or '',
        }
    )


    bot.reply_to(
        message,
        f'Привет, {message.from_user.full_name}! 👋\n\n'
        f'Я помогу тебе спланировать поездку:\n\n'
        f'🌤 Узнать погоду в любом городе мира\n'
        f'✈️ Найти дешёвые авиабилеты и сразу перейти к покупке\n'
        f'📋 Сохраню историю твоих запросов\n\n'
        f'Выбери что тебя интересует:',
        reply_markup=main_menu()
    )