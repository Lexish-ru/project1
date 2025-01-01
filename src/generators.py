from typing import Dict, Generator, List


def filter_by_currency(transactions: List[Dict], currency: str) -> Generator[Dict, None, None]:
    """Генератор для фильтрации транзакций по валюте"""
    for transaction in transactions:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency:
            yield transaction


def transaction_descriptions(transactions: List[Dict]) -> Generator[str, None, None]:
    """Генератор для получения описания транзакции"""
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """Генератор номера карты"""
    for num in range(start, end + 1):
        card_number = f"{num:016d}"
        yield f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}"
