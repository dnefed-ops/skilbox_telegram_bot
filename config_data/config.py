import os
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / '.env'

if not env_path.exists():
    exit('Переменные окружения не загружены т.к. отсутствует файл .env')

load_dotenv(env_path)

BOT_TOKEN = os.getenv('BOT_TOKEN')
TRAVELPAYOUTS_TOKEN = os.getenv('TRAVELPAYOUTS_TOKEN')
DEFAULT_COMMANDS = (
    ('start', 'Запустить бота'),
    ('help', 'Вывести справку'),
    ('weather', 'Узнать погоду в любом городе.')
)