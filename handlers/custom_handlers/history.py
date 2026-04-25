from telebot.types import Message
from loader import bot
from database.config import db, User, Request
from keyboards.reply.main_menu import main_menu


@bot.message_handler(func=lambda m: m.text == '📋 История запросов')
def menu_history(message: Message) -> None:
    with db:
        user = User.get_or_none(User.telegram_id == message.from_user.id)
        if not user:
            bot.reply_to(message, '📋 У вас пока нет истории запросов.',
                         reply_markup=main_menu()
            )
            return

        request =  (Request
                    .select()
                    .where(Request.user_id == user.id)
                    .order_by(Request.created_at.desc())
                    .limit(10))

        if not request:
            bot.reply_to(message, '📋 У вас пока нет истории запросов.',
                         reply_markup=main_menu())
            return

        text = '📋 <b>Последние 10 запросов:</b>\n\n'
        for i, req in enumerate(request, 1):
            date = req.created_at.strftime('%d.%m.%Y %H:%M')
            text += f'{i}. 🏙 <b>{req.request}</b> — {req.answer_request}\n<i>{date}</i>\n\n'

        bot.send_message(message.chat.id, text, parse_mode='HTML',
                         reply_markup=main_menu())