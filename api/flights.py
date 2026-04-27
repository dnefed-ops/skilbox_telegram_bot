import requests
from typing import Optional, List, Dict

from config_data import config


FLIGHTS_API_URL = 'https://api.travelpayouts.com/v1/prices/calendar'


def search_flights(origin: str, destination: str, depart_date: str, sort: str =
                   'cheap') -> Optional[list[Dict]]:
    """
        Ищет билеты на каждый день указанного месяца через /v1/prices/calendar.
        depart_date — строка ГГГГ-ММ-ДД или ГГГГ-ММ.
        sort — 'cheap' (дешёвые) или 'expensive' (дорогие).
        Возвращает список словарей с данными по билетам или None при ошибке. [web:16]
        """
    depart_month = depart_date[:7]

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
        print(f'Encoding: {response.headers.get("Content-Encoding")}')
        print(f'DEBUG API ответ: {data}')

        if not data.get('success'):
            print(f'Ошибка Travelpayouts: success=False, data={data}')
            return None

        results: List[Dict] = []
        for date_key, info, in data.get('data', {}).items():
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
