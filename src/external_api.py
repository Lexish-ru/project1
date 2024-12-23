from typing import Union

import requests

from src.utils import get_or_create_api_key

EXCHANGE_API_URL = "https://api.apilayer.com/exchangerates_data/convert"
API_KEY = get_or_create_api_key()


def convert_to_rub(amount: Union[int, float], currency_code: str) -> float:
    """
    Конвертирует сумму из указанной валюты в рубли.
    """
    if currency_code == "RUB":
        return float(amount)

    params = {
        "from": currency_code,
        "to": "RUB",
        "amount": amount
    }
    headers = {"apikey": API_KEY}

    try:
        response = requests.get(EXCHANGE_API_URL, params=params, headers=headers)
        response.raise_for_status()
        result = response.json()
        return float(result.get("result", 0.0))
    except requests.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return 0.0
    except KeyError as e:
        print(f"Ошибка при обработке ответа API: {e}")
        return 0.0
