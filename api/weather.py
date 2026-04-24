import requests
from typing import Optional


def get_weather(lat: float, lon: float) -> Optional[dict]:
    """ТПолучает текущую погоду по координатам.
    Возвращает словарь с данными или None при ошибке."""


    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': lat,
        'longitude': lon,
        'current_weather': 'true',
        'timezone': 'auto',
        'wind_speed_unit': 'kmh'
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        current = data['current_weather']

        return {
            'temperature': current['temperature'],
            'wind_speed': current['windspeed'],
            'description': _weather_description(current['weathercode'])
        }
    
    except Exception as exc:
        print(f"ошибка получения данных погоды: {exc}")
        return None
    

def _weather_description(code: int) -> str:
    """Расшифровка кода погоды open-meteo в текст."""
    codes = {
        0: '☀️ Ясно',
        1: '🌤 Преимущественно ясно',
        2: '⛅️ Переменная облачность',
        3: '☁️ Пасмурно',
        45: '🌫 Туман',
        48: '🌫 Туман с инеем',
        51: '🌦 Лёгкая морось',
        53: '🌦 Морось',
        55: '🌧 Сильная морось',
        61: '🌧 Небольшой дождь',
        63: '🌧 Дождь',
        65: '🌧 Сильный дождь',
        71: '🌨 Небольшой снег',
        73: '🌨 Снег',
        75: '❄️ Сильный снег',
        80: '🌦 Ливень',
        81: '🌧 Сильный ливень',
        95: '⛈ Гроза',
        99: '⛈ Гроза с градом',
    }
    return codes.get(code, '🌡 Данные получены')