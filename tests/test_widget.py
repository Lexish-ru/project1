import pytest

from src.widget import get_date, mask_card_account


def test_mask_card_account() -> None:
    """Тест функции обработки номера карты и счёта"""
    assert mask_card_account("Visa 1234567812345678") == "Visa 1234 56** **** 5678"
    assert mask_card_account("Счет 12345678901234567890") == "Cчёт **7890"
    with pytest.raises(ValueError, match="Некорректный номер карты"):
        mask_card_account("Visa 1234abcd5678efgh")
    with pytest.raises(ValueError, match="Некорректные данные"):
        mask_card_account("UnknownData")


def test_get_date():
    """Тест функции конвертации даты"""
    assert get_date("2024-12-23") == "23.12.2024"
    assert get_date("Invalid date") == "Неизвестно"

