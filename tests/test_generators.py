from typing import Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


def test_filter_by_currency(generators_transactions_fixture: List[Dict]) -> None:
    """Тестирование функции filter_by_currency"""
    usd_transactions = list(filter_by_currency(generators_transactions_fixture, "USD"))
    assert len(usd_transactions) == 2
    assert usd_transactions[0]["description"] == "Перевод организации"
    assert usd_transactions[1]["description"] == "Перевод со счета на счет"

    eur_transactions = list(filter_by_currency(generators_transactions_fixture, "EUR"))
    assert len(eur_transactions) == 1

    empty_transactions: List[Dict] = []  # Аннотируем тип как список словарей
    empty_result = list(filter_by_currency(empty_transactions, "USD"))
    assert len(empty_result) == 0


def test_transaction_descriptions(generators_transactions_fixture: List[Dict]) -> None:
    """Тестирование функции transaction_descriptions"""
    descriptions = list(transaction_descriptions(generators_transactions_fixture))
    assert descriptions == ["Перевод организации", "Перевод со счета на счет", "Перевод с карты на карту"]

    empty_descriptions = list(transaction_descriptions([]))
    assert empty_descriptions == []


@pytest.mark.parametrize("start, end, expected", [
    (1, 5, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003",
            "0000 0000 0000 0004", "0000 0000 0000 0005"]),
    (100, 102, ["0000 0000 0000 0100", "0000 0000 0000 0101", "0000 0000 0000 0102"])
])
def test_card_number_generator(start: int, end: int, expected: List[str]) -> None:
    """Тестирование функции card_number_generator"""
    generated_numbers = list(card_number_generator(start, end))
    assert generated_numbers == expected
