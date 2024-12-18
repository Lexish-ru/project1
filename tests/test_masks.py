from typing import List, Tuple

from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number(card_test_data: List[Tuple[str, str]]) -> None:
    """Тест функции маскировки номера карты"""
    for card_number, expected in card_test_data:
        assert get_mask_card_number(card_number) == expected


def test_get_mask_account(account_test_data: List[Tuple[str, str]]) -> None:
    """Тест функции маскировки номера счёта"""
    for bank_account, expected in account_test_data:
        assert get_mask_account(bank_account) == expected
