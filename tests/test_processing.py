import os
from typing import List
from unittest.mock import patch

import pandas as pd
import pytest

from src.processing import (filter_by_state, read_transactions_from_csv, read_transactions_from_excel,
                            sort_by_date, search_transactions_by_description, categorize_transactions_by_description)


@pytest.mark.parametrize(
    "state, expected",
    [
        (
            "EXECUTED",
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
        (
            "CANCELED",
            [
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
        ),
        ("PENDING", []),
    ],
)
def test_filter_by_state(transactions_fixture: List[dict], state: str, expected: List[dict]) -> None:
    """Тест функции сортировки по статусу транзакции"""
    assert filter_by_state(transactions_fixture, state) == expected


@pytest.mark.parametrize(
    "transactions_fixture, reverse, expected",
    [
        (
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
            True,
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
        (
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            False,
            [
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            ],
        ),
    ],
)
def test_sort_by_date(transactions_fixture: List[dict], reverse: bool, expected: List[dict]) -> None:
    """Тест функции сортировки по дате"""
    assert sort_by_date(transactions_fixture, reverse) == expected


def test_sort_by_date_invalid_data() -> None:
    """Тест функции сортировки по дате с заведомо неверными данными"""
    with pytest.raises(ValueError):
        sort_by_date([{"invalid": "data"}])


def test_read_transactions_from_csv():
    """Тест функции чтения данных из CSV."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    test_file = os.path.join(base_dir, "transactions.csv")

    expected_output = [
        {
            "id": "650703",
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 16210,
            "currency_name": "Sol",
            "currency_code": "PEN",
            "from": "Счет 58803664561298323391",
            "to": "Счет 39745660563456619397",
            "description": "Перевод организации",
        },
        {
            "id": "3598919",
            "state": "EXECUTED",
            "date": "2020-12-06T23:00:58Z",
            "amount": 29740,
            "currency_name": "Peso",
            "currency_code": "COP",
            "from": "Discover 3172601889670065",
            "to": "Discover 0720428384694643",
            "description": "Перевод с карты на карту",
        },
    ]

    result = read_transactions_from_csv(test_file)
    for idx, (expected, actual) in enumerate(zip(expected_output, result)):
        assert expected["id"] == actual["id"]
        assert expected["amount"] == actual["amount"]

    print("Test passed for CSV file.")


def test_read_transactions_from_excel():
    """Тест функции чтения данных из Excel."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    test_file = os.path.join(base_dir, "transactions_excel.xlsx")

    expected_output = [
        {
            "id": "650703",
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 16210,
            "currency_name": "Sol",
            "currency_code": "PEN",
            "from": "Счет 58803664561298323391",
            "to": "Счет 39745660563456619397",
            "description": "Перевод организации",
        },
        {
            "id": "3598919",
            "state": "EXECUTED",
            "date": "2020-12-06T23:00:58Z",
            "amount": 29740,
            "currency_name": "Peso",
            "currency_code": "COP",
            "from": "Discover 3172601889670065",
            "to": "Discover 0720428384694643",
            "description": "Перевод с карты на карту",
        },
    ]

    print(f"Using file: {test_file}")  # Проверяем путь к файлу
    result = read_transactions_from_excel(test_file)

    # Приводим id к строке для унификации
    for transaction in result:
        transaction["id"] = str(transaction["id"])

    for idx, (expected, actual) in enumerate(zip(expected_output, result)):
        for key in expected:
            assert expected[key] == actual.get(key), (
                f"Key: {key} |" f" Expected: {expected[key]} |" f" Actual: {actual.get(key)}"
            )

    print("Test passed for Excel file.")


@patch("pandas.read_csv")
def test_read_transactions_from_csv_mock(mock_read_csv):
    """Тест функции чтения данных из CSV с использованием Mock."""
    mock_data = pd.DataFrame(
        [
            {
                "id": "650703",
                "state": "EXECUTED",
                "date": "2023-09-05T11:30:32Z",
                "amount": 16210,
                "currency_name": "Sol",
                "currency_code": "PEN",
                "from": "Счет 58803664561298323391",
                "to": "Счет 39745660563456619397",
                "description": "Перевод организации",
            },
            {
                "id": "3598919",
                "state": "EXECUTED",
                "date": "2020-12-06T23:00:58Z",
                "amount": 29740,
                "currency_name": "Peso",
                "currency_code": "COP",
                "from": "Discover 3172601889670065",
                "to": "Discover 0720428384694643",
                "description": "Перевод с карты на карту",
            },
        ]
    )

    mock_read_csv.return_value = mock_data

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    test_file = os.path.join(base_dir, "transactions.csv")

    result = read_transactions_from_csv(test_file)

    assert len(result) == 2
    assert result[0]["id"] == "650703"
    assert result[1]["id"] == "3598919"

    print("Mock test passed for CSV.")


@patch("pandas.read_excel")
def test_read_transactions_from_excel_mock(mock_read_excel):
    """Тест функции чтения данных из Excel с использованием Mock."""
    mock_data = pd.DataFrame(
        [
            {
                "id": "650703",
                "state": "EXECUTED",
                "date": "2023-09-05T11:30:32Z",
                "amount": 16210,
                "currency_name": "Sol",
                "currency_code": "PEN",
                "from": "Счет 58803664561298323391",
                "to": "Счет 39745660563456619397",
                "description": "Перевод организации",
            },
            {
                "id": "3598919",
                "state": "EXECUTED",
                "date": "2020-12-06T23:00:58Z",
                "amount": 29740,
                "currency_name": "Peso",
                "currency_code": "COP",
                "from": "Discover 3172601889670065",
                "to": "Discover 0720428384694643",
                "description": "Перевод с карты на карту",
            },
        ]
    )

    mock_read_excel.return_value = mock_data

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    test_file = os.path.join(base_dir, "transactions_excel.xlsx")

    result = read_transactions_from_excel(test_file)

    assert len(result) == 2
    assert result[0]["id"] == "650703"
    assert result[1]["id"] == "3598919"

    print("Mock test passed for Excel.")


# Тестовая функция для проверки корректности работы
if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    test_file = os.path.join(base_dir, "transactions_excel.xlsx")
    result = read_transactions_from_excel(test_file)
    print(result[:2])  # Вывод первых двух записей

def test_search_transactions_by_description():
    transactions = [
        {"id": 1, "description": "Payment for invoice 12345"},
        {"id": 2, "description": "Transfer to account 67890"},
        {"id": 3, "description": "Payment received from ABC Corp."},
    ]

    # Поиск строки, которая точно есть
    result = search_transactions_by_description(transactions, "payment")
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3

    # Поиск строки с учетом регистра
    result = search_transactions_by_description(transactions, "PAYMENT")
    assert len(result) == 2

    # Поиск строки, которой нет в описании
    result = search_transactions_by_description(transactions, "nonexistent")
    assert len(result) == 0

    # Поиск с пустой строкой
    result = search_transactions_by_description(transactions, "")
    assert len(result) == 3

    def test_categorize_transactions_by_description():
        transactions = [
            {"id": 1, "description": "Payment for invoice"},
            {"id": 2, "description": "Transfer to account"},
            {"id": 3, "description": "Payment received"},
            {"id": 4, "description": "Refund for invoice"},
        ]
        categories = ["payment", "transfer", "refund"]

        result = categorize_transactions_by_description(transactions, categories)
        assert result == {"payment": 2, "transfer": 1, "refund": 1}

        # Проверка с пустым списком транзакций
        result = categorize_transactions_by_description([], categories)
        assert result == {"payment": 0, "transfer": 0, "refund": 0}

        # Проверка с пустым списком категорий
        result = categorize_transactions_by_description(transactions, [])
        assert result == {}

        # Проверка на отсутствие совпадений
        result = categorize_transactions_by_description(transactions, ["nonexistent"])
        assert result == {"nonexistent": 0}
