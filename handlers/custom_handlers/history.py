from telebot.types import Message
from loader import bot
from database.config import db, User, Request
from keyboards.reply.main_menu import main_menu
from keyboards.reply.history_menu import history_menu


@bot.message_handler(func=lambda m: m.text == '📋 История запросов')
def menu_history(message: Message) -> None:
    bot.send_message(
        message.chat.id,
        '📋 Выберите тип истории:',
        reply_markup=history_menu()
    )

@bot.message_handler(func=lambda m: m.text == '🌤 История погоды')
def history_weather(message: Message) -> None:
    user = User.get_or_none(User.telegram_id == message.from_user.id)
    if not user:
        bot.send_message(
            message.chat.id,
            '❌ Пользователь не найден.',
            reply_markup=main_menu()
        )
        return

    requests = (Request
                .select()
                .where((Request.user_id == user.id) & (Request.request_type ==
                                                      'weather'))
                .order_by(Request.created_at.desc())
                .limit(5))

    if not requests:
        bot.send_message(
            message.chat.id,
            '📭 История погоды пуста. Сделайте хотя бы один успешный поиск погоды.',
            reply_markup=main_menu()
        )
        return

    lines = ['🌤 <b>Последние запросы погоды:</b>\n']
    for i, r in enumerate(requests, 1):
        lines.append(
            f'{i}. 🏙 {r.request}\n'
            f'   {r.answer_request}\n'
            f'   🕐 {r.created_at.strftime("%d.%m.%Y %H:%M")}\n'
        )

    bot.send_message(
        message.chat.id,
        '\n'.join(lines),
        parse_mode='HTML',
        reply_markup=main_menu()
    )


@bot.message_handler(func=lambda m: m.text == '✈️ История билетов')
def history_flights(message: Message) -> None:
    user = User.get_or_none(User.telegram_id == message.from_user.id)
    if not user:
        bot.send_message(
            message.chat.id,
            '❌ Пользователь не найден.',
            reply_markup=main_menu()
        )
        return

    requests = (Request
                .select()
                .where((Request.user_id == user.id) & (Request.request_type =='flight'))
                .order_by(Request.created_at.desc())
                .limit(5))

    if not requests:
        bot.send_message(
            message.chat.id,
            '📭 История билетов пуста. Сделайте хотя бы один успешный поиск билетов.',
            reply_markup=main_menu()
        )
        return

    lines = ['✈️ <b>Последние запросы билетов:</b>\n']
    for i, r in enumerate(requests, 1):
        lines.append(
            f'{i}. 🗺 {r.request}\n'
            f'   {r.answer_request}\n'
            f'   🕐 {r.created_at.strftime("%d.%m.%Y %H:%M")}\n'
        )

    bot.send_message(
        message.chat.id,
        '\n'.join(lines),
        parse_mode='HTML',
        reply_markup=main_menu()
    )