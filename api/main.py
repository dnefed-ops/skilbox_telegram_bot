import requests
import json
from location import get_location, POPULAR_CITIES


def get_weather(lat: float, lon: float) -> float:
    """Текущая температура"""
    url = f'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': lat,
        'longitude': lon,
        'current_weather': 'true',
        'timezone': 'auto'
    }

    response = requests.get(url, params=params)
    data = response.json()
    return data['current_weather']['temperature']


print('🌤️ Погодный консольный бот готов!')
print( f'Выход: "exit" или Ctrl+C\n')
print( f'Список городов "список"\n')


while True:
    try:
        city = input('Введите название города (Ru/En): ').strip().capitalize()
        if city.lower() in ['exit', 'выход', 'quit']:
            print('\n👋 Пока!')
            break
        if city.lower() == 'список':
            print(POPULAR_CITIES)

        coordinates_city = get_location(city)
        if coordinates_city:
            city_lat, city_lon = coordinates_city
            temperature = get_weather(lat=city_lat,  lon=city_lon)
            print(f'🌡️ Текущая температура в {city}: **{temperature}°C**\n')
        else:
            print('Попробуйте другой город (Москва, Moskow, Mskva...)\n')

    except KeyboardInterrupt:
        print('\n👋 Пока!')
    except Exception as exc:
        print(f'Ошибка: {exc}')