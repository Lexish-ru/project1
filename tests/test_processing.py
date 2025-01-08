import os
from typing import List
from unittest.mock import patch

import pandas as pd
import pytest

from src.processing import (
    filter_by_state,
    read_transactions_from_csv,
    read_transactions_from_excel,
    sort_by_date,
    categorize_transactions_by_description,
    search_transactions_by_regex,
)


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
def test_sort_by_date(transactions_fixture, reverse, expected):
    result = sort_by_date(transactions_fixture, reverse)
    assert result == expected


def test_sort_by_date_invalid_data():
    transactions = [{"invalid": "data"}]  # Транзакция без ключа "date"
    with pytest.warns(UserWarning, match="Некорректная дата в транзакции"):
        result = sort_by_date(transactions, reverse=True)
    assert len(result) == 0  # Все некорректные транзакции должны быть отфильтрованы


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


@pytest.mark.parametrize(
    "transactions, categories, expected",
    [
        (
            [{"description": "Grocery store payment"}, {"description": "Online shopping"}],
            ["grocery", "shopping"],
            {"grocery": 1, "shopping": 1},
        ),
        ([{"description": ""}], ["grocery"], {"grocery": 0}),
    ],
)
def test_categorize_transactions_by_description(transactions, categories, expected):
    assert categorize_transactions_by_description(transactions, categories) == expected


@pytest.mark.parametrize(
    "transactions, search_term, expected",
    [
        (
            [{"description": "Payment for coffee"}, {"description": "Lunch payment"}],
            "Payment",
            [{"description": "Payment for coffee"}, {"description": "Lunch payment"}],
        ),
        ([{"description": "Coffee"}, {"description": ""}], "Lunch", []),
    ],
)
def test_search_transactions_by_regex(transactions, search_term, expected):
    assert search_transactions_by_regex(transactions, search_term) == expected
