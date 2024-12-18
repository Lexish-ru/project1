from io import StringIO
from pathlib import Path
from typing import Dict, Generator, List, Tuple, Union
from unittest.mock import patch
import os

import random

import pytest


@pytest.fixture
def transactions_fixture() -> List[Dict[str, Union[int, str, Dict[str, str]]]]:
    """Тестовые данные с транзакциями"""
    return [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]


@pytest.fixture
def card_test_data() -> List[Tuple[str, str]]:
    """Тестовые данные с номерами карт"""
    return [
        ("1234567891234567", "1234 56** **** 4567"),
        ("1111222233334444", "1111 22** **** 4444"),
        ("12345", "Введённые Вами данные не соответсвуют формату номера банковской карты"),
        ("12345678901234567890", "Введённые Вами данные не соответсвуют формату номера банковской карты"),
        ("abcd1234efgh5678", "Введённые Вами данные не соответсвуют формату номера банковской карты"),
        ("", "Введённые Вами данные не соответсвуют формату номера банковской карты")
    ]


@pytest.fixture
def account_test_data() -> List[Tuple[str, str]]:
    """Тестовые данные с номерами счетов"""
    return [
        ("12345678901234567890", "**7890"),
        ("00000000000000000000", "**0000"),
        ("1234567890", "Введённые Вами данные не соответсвуют формату номера банковского счёта."),
        ("123456789012345678901234", "Введённые Вами данные не соответсвуют формату номера банковского счёта."),
        ("abcd1234efgh56789012", "Введённые Вами данные не соответсвуют формату номера банковского счёта."),
        ("", "Введённые Вами данные не соответсвуют формату номера банковского счёта.")
    ]


@pytest.fixture
def mask_card_account_test_data() -> List[Tuple[str, Union[str, type]]]:
    """Тестовые данные с указанием счетов и карт"""
    return [
        # Корректные данные для счета
        ("Счет 12345678901234567890", "Cчёт **7890"),
        ("Счет 00000000000000000000", "Cчёт **0000"),

        # Корректные данные для карт
        ("Visa Platinum 1234567890123456", "Visa Platinum 1234 56** **** 3456"),
        ("Maestro 1111222233334444", "Maestro 1111 22** **** 4444"),

        # Некорректные данные
        ("Некорректные данные", ValueError),
        ("Visa1234567890", ValueError),
        ("Счет 12345", ValueError),
    ]


@pytest.fixture
def get_date_test_data() -> List[Tuple[str, Union[str, type]]]:
    """Тестовые данные с датами"""
    return [
        # Корректные даты
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-01-01", "01.01.2023"),

        # Некорректные данные
        ("", ValueError),
        ("2023-13-01", ValueError),
        ("Некорректные данные", ValueError),
    ]


@pytest.fixture
def generators_transactions_fixture() -> List[Dict[str, Union[int, str, Dict[str, Union[str, Dict[str, str]]]]]]:
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 123456789,
            "state": "PENDING",
            "date": "2020-01-01T00:00:00.000000",
            "operationAmount": {"amount": "1000", "currency": {"name": "EUR", "code": "EUR"}},
            "description": "Перевод с карты на карту",
            "from": "Счет 123456789",
            "to": "Счет 987654321"
        }
    ]


@pytest.fixture
def mock_console_log() -> Generator[StringIO, None, None]:
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        yield mock_stdout


@pytest.fixture
def mock_file_log(tmp_path: Path) -> Generator[Path, None, None]:
    log_file = tmp_path / "test.log"
    yield log_file

LOG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/mylog.txt"))

@pytest.fixture(autouse=True)
def cleanup_log_file() -> None:
    """Удаляет лог-файл перед каждым тестом."""
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
