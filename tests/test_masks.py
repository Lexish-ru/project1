import pytest

from src.masks import mask_bank_account, mask_card_number


def test_mask_card_number():
    """Тест функции маскировки номера карты"""
    assert mask_card_number("1234567812345678") == "1234 56** **** 5678"
    assert mask_card_number("8765432187654321") == "8765 43** **** 4321"
    assert mask_card_number("123456781234567") == "1234 ****** 4567"  # Для карт American Express
    with pytest.raises(ValueError, match="Неверный формат номера банковской карты"):
        mask_card_number("1234abcd5678efgh")
    with pytest.raises(ValueError, match="Неверный формат номера банковской карты"):
        mask_card_number("12345678")


def test_mask_bank_account():
    """Тест функции маскировки номера счёта"""
    assert mask_bank_account("12345678901234567890") == "**7890"
    assert mask_bank_account("09876543210987654321") == "**4321"
    with pytest.raises(ValueError, match="Неверный формат номера банковского счёта"):
        mask_bank_account("abcd1234abcd5678abcd")
    with pytest.raises(ValueError, match="Неверный формат номера банковского счёта"):
        mask_bank_account("12345678")
