import time
from typing import List, Optional, Tuple

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from rapidfuzz import process, fuzz


POPULAR_CITIES: list[str] = [
    "Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург",
    "Краснодар", "Красноярск", "Нижний Новгород", "London", "New York"
]

geolocator = Nominatim(user_agent='weather_bot_simple')

def get_location(city: str) -> Optional[List[float]]:
    """Возвращает [lat, lon] или None. Авто-добавляет найденные города."""
    city = city.strip()
    if not city:
        return None

    time.sleep(1.1)

    try:
        if city in POPULAR_CITIES:
            location = geolocator.geocode(city, language='ru', timeout=10)
            if location:
                return [location.latitude, location.longitude]

        location = geolocator.geocode(city, language='ru', timeout=10)
        if location:
            if city not in POPULAR_CITIES:
                POPULAR_CITIES.append(city)
                print(f'✅ "{city}" добавлен в базу ({len(POPULAR_CITIES)} городов).')
            return [location.latitude, location.longitude]

        match: str
        score: float
        _: int
        match, score, _ = process.extractOne(city, POPULAR_CITIES, scorer=fuzz.ratio)
        if score > 85:
            print(f"🔍 Думаю тут опечатка '{city}' исправил на '{match}' отличие в буквах ({score:.0f}%)")
            location = geolocator.geocode(match, language='ru', timeout=10)
            if location:
                return [location.latitude, location.longitude]
        print(f'❌ Город "{city}" не найден')
        return None

    except (GeocoderTimedOut, GeocoderUnavailable) as exc:
        print("⏱️ Сервис недоступен, попробуйте позже", exc)
        return None
    except Exception as exc:
        print(f"❌ Ошибка: {exc}")
        return None

test = get_location('Мекха')
print(test)