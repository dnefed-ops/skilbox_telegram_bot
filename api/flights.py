import requests
from typing import Optional, List, Dict

from config_data import config


FLIGHTS_API_URL = 'https://api.travelpayouts.com/v1/prices/cheap'


def search_flights(origin: str, destination: str, depart_date: str) -> Optional[list[Dict]]:
    """
        Ищет самые дешёвые авиабилеты на дату вылета.
        origin, destination – IATA-коды городов (например: MOW, KJA, LED).
        depart_date – строка в формате 'ГГГГ-ММ-ДД' или 'ГГГГ-ММ' (API допускает месяц). [web:26][web:20]
        Возвращает список словарей с данными по билетам или None при ошибке. [web:16]
        """
    params = {
        'origin': origin.upper(),
        'destination': destination.upper(),
        'depart_date': depart_date,
        'token': config.TRAVELPAYOUTS_TOKEN,
        'currency': 'rub',
        'page': 1,
        'limit': 5,
    }

    try:
        response = requests.get(FLIGHTS_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get('success'):
            print(f'Ошибка Travelpayouts: success=False, data={data}')
            return None

        prices = data.get('data', {})
        # data['data'] – словарь: { 'DEST': { 'DATE': {...}, ... } } [web:26]
        results: List[Dict] = []

        for dest_code, flights_by_date, in prices.items():
            for _, info in flights_by_date.items():
                results.append({
                    'price': info.get('price'),
                    'airline': info.get('airline'),
                    'flight_number': info.get('flight_number'),
                    'departure_at': info.get('departure_at'),
                    'return_at': info.get('return_at'),
                    'transfers': info.get('transfers')
                })

        results.sort(key=lambda x: x.get('price') or 10**9)
        return results[:5]

    except Exception as exc:
        print(f'Ошибка запроса к Travelpayouts: {exc}')
        return None
