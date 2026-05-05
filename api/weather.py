import requests
from typing import Optional


GEOCODING_URL = 'https://geocoding-api.open-meteo.com/v1/search'
WEATHER_URL = 'https://api.open-meteo.com/v1/forecast'

WMO_CODES = {
    0: ('☀️', 'Ясно'),
    1: ('🌤', 'Преимущественно ясно'),
    2: ('⛅️', 'Переменная облачность'),
    3: ('☁️', 'Пасмурно'),
    45: ('🌫', 'Туман'),
    48: ('🌫', 'Туман с инеем'),
    51: ('🌦', 'Лёгкая морось'),
    53: ('🌦', 'Морось'),
    55: ('🌧', 'Сильная морось'),
    61: ('🌧', 'Небольшой дождь'),
    63: ('🌧', 'Дождь'),
    65: ('🌧', 'Сильный дождь'),
    71: ('🌨', 'Небольшой снег'),
    73: ('🌨', 'Снег'),
    75: ('❄️', 'Сильный снег'),
    77: ('🌨', 'Снежная крупа'),
    80: ('🌦', 'Ливень'),
    81: ('🌧', 'Сильный ливень'),
    82: ('⛈', 'Очень сильный ливень'),
    85: ('🌨', 'Снегопад'),
    86: ('🌨', 'Сильный снегопад'),
    95: ('⛈', 'Гроза'),
    96: ('⛈', 'Гроза с градом'),
    99: ('⛈', 'Гроза с сильным градом'),
}


def get_city_coordinates(city: str) -> Optional[dict]:
    """
    Ищет город по названию. Возвращает dict с name, country, lat, lon
    или None если не нашёл.
    """
    params = {
        'name': city,
        'count': 1,
        'language': 'ru',
        'format': 'json',
    }
    try:
        response = requests.get(GEOCODING_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get('results'):
            return None  # ✅ город не найден

        result = data['results'][0]
        return {
            'name': result.get('name', city),
            'country': result.get('country', ''),
            'lat': result['latitude'],
            'lon': result['longitude'],
        }
    except Exception as exc:
        print(f'Ошибка геокодинга: {exc}')
        return None


def get_weather(lat: float, lon: float) -> Optional[dict]:
    """Получает текущую погоду по координатам."""
    params = {
        'latitude': lat,
        'longitude': lon,
        'current_weather': 'true',
        'timezone': 'auto',
        'wind_speed_unit': 'kmh',
    }
    try:
        response = requests.get(WEATHER_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        current = data['current_weather']
        icon, description = WMO_CODES.get(current['weathercode'], ('🌡', 'Неизвестно'))

        return {
            'temperature': current['temperature'],
            'wind_speed': current['windspeed'],
            'description': description,
            'icon': icon,
        }
    except Exception as exc:
        print(f'Ошибка получения погоды: {exc}')
        return None