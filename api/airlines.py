import requests


_AIRLINES_CACHE: dict[str, str] = {}

def load_airlines() -> dict[str, str]:
    """Загружает справочник авиакомпаний и кэширует в памяти."""
    global _AIRLINES_CACHE
    if _AIRLINES_CACHE:
        return _AIRLINES_CACHE  #Уже загружен - повторно не запрашиваем.

    try:
        response = requests.get(
            'https://api.travelpayouts.com/data/ru/airlines.json',
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        _AIRLINES_CACHE = {
            item['code']: item.get('name', item['code'])
            for item in data
            if item.get['code'] and item.get('name')
        }
    except Exception as exc:
        print(f'Ошибка загрузки справочника авиакомпаний: {exc}')

    return _AIRLINES_CACHE


def get_airline_name(code: str) -> str:
    """По коду IATA возвращает название авиакомпании на русском."""
    airlines = load_airlines()
    return airlines.get(code, code) #Если не нашел компанию, вернем код.