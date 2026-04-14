from telebot.types import Message
from loader import bot
from api import location


def get_user_data(data):
    data = input('Введите Город: ')

@bot.message_handler(commands=['weather'])
def bot_weather(message: Message):
    bot.reply_to(message, f'Привет, Пробуем дать тебе погоду {message.from_user.full_name}!')

