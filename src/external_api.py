import os
from typing import Union

import requests
from dotenv import load_dotenv

load_dotenv()

EXCHANGE_API_URL = "https://api.apilayer.com/exchangerates_data/convert"
API_KEY = os.getenv("EXCHANGE_API_KEY")


def convert_to_rub(amount: Union[int, float], currency_code: str) -> float:
    """
    Конвертирует сумму в рубли, используя внешний API.

    :param amount: Сумма для конвертации.
    :param currency_code: Код валюты (например, "USD", "EUR").
    :return: Сумма в рублях.
    """
    if currency_code == "RUB":
        return float(amount)
    if not API_KEY:
        raise EnvironmentError("API ключ для конвертации валют не найден.")

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
        return float(result["result"])
    except (requests.RequestException, KeyError) as e:
        print(f"Ошибка при конвертации валюты: {e}")
        return 0.0
