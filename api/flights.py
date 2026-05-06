import requests
from typing import Optional, List, Dict

from config_data import config


FLIGHTS_API_URL = 'https://api.travelpayouts.com/v1/prices/calendar'


def build_aviasales_link(origin: str, destination: str, departure_at: str) -> str:
    """Формирует ссылку на покупку билета через Travelpayouts.
    За каждую покупку по этой ссылке начисляется вознаграждение.
    """
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(departure_at)
        date_str = dt.strftime('%Y-%m-%d') # Формат: YYYY-MM-DD
    except Exception:
        date_str =  ''

    marker = config.TRAVELPAYOUTS_MARKER   # Ваш партнерский маркер.

    url = (
        f'https://search.aviasales.ru/?'
        f'origin_iata={origin}'
        f'&destination_iata={destination}'
        f'&depart_date={date_str}'
        f'&adults=1'
        f'&marker={marker}'
    )

    return url


def search_flights(origin: str, destination: str, depart_date: str, sort: str =
                   'cheap') -> Optional[list[Dict]]:
    """
        Ищет билеты на каждый день указанного месяца через /v1/prices/calendar.
        depart_date — строка ГГГГ-ММ-ДД или ГГГГ-ММ.
        sort — 'cheap' (дешёвые) или 'expensive' (дорогие).
        Возвращает список словарей с данными по билетам или None при ошибке. [web:16]
        """
    if not origin or not destination:
        return None

    depart_month = depart_date[:7] # '2026-05'

    params = {
        'origin': origin.upper(),
        'destination': destination.upper(),
        'depart_date': depart_month,
        'calendar_type': 'departure_date',
        'currency': 'rub',
        'token': config.TRAVELPAYOUTS_TOKEN,
    }

    try:
        response = requests.get(FLIGHTS_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get('success'):
            print(f'Ошибка Travelpayouts: success=False, data={data}')
            return None

        results: List[Dict] = []
        for date_key, info, in data.get('data', {}).items():

            # Фильтруем только билеты запрашиваемого месяца.
            if not date_key.startswith(depart_month):
                continue

            results.append({
                'price': info.get('price'),
                'airline': info.get('airline'),
                'flight_number': info.get('flight_number'),
                'departure_at': info.get('departure_at', date_key),
                'transfers': info.get('transfers', 0),
            })

        if not results:
            return None

        reverse = (sort == 'expensive')
        results.sort(key=lambda x: x.get('price') or 10**9, reverse=reverse)
        return results[:5]

    except Exception as exc:
        print(f'Ошибка запроса к Travelpayouts: {exc}')
        return None
