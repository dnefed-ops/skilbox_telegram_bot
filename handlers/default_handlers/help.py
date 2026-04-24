from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS
from loader import bot
from keyboards.reply import main_menu


@bot.message_handler(commands=['help'])
def bot_help(message: Message)-> None:
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, '\n'.join(text), reply_markup=main_menu())