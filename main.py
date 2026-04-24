from loader import bot
import handlers
from utils.set_bot_commands import set_default_commands
from database.config import initialize_db


if __name__ == '__main__':
    initialize_db()
    set_default_commands(bot)
    print('Бот запущен...')


    @bot.message_handler(func=lambda m: True)
    def catch_all(m):
        print(f'CATCH ALL: {m.text}')


    bot.infinity_polling(allowed_updates=['message'], skip_pending=True,
                         timeout=30)