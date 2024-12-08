from typing import List, Tuple, Union

import pytest

from src.widget import get_date, mask_card_account


def test_mask_card_account(mask_card_account_test_data: List[Tuple[str, Union[str, type]]]) -> None:
    """Тест функции маскировки номера карты или счёта"""
    for number_import, expected in mask_card_account_test_data:
        if isinstance(expected, type) and issubclass(expected, Exception):
            with pytest.raises(expected):
                mask_card_account(number_import)
        else:
            assert mask_card_account(number_import) == expected


def test_get_date(get_date_test_data: List[Tuple[str, Union[str, type]]]) -> None:
    """Тест функции получения даты в читаемом виде из строки транзакции"""
    for date, expected in get_date_test_data:
        if isinstance(expected, type) and issubclass(expected, Exception):
            with pytest.raises(expected):
                get_date(date)
        else:
            assert get_date(date) == expected
