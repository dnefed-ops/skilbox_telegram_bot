import requests


def get_iata_code(city_name: str) -> str:
    """
    По названию города возвращает IATA-код аэропорта.
    Например: 'Москва' → 'MOW', 'Красноярск' → 'KJA'
    """
    url = 'https://autocomplete.travelpayouts.com/places2'
    params = {
        'term': city_name,
        'locate': 'ru',
        'types[]': 'city',
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data:
            return data[0].get('code')
    except Exception as exc:
        print(f'Ошибка поиска города: {exc}')
    return None