from typing import List

import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize(
    "state, expected",
    [
        ("EXECUTED", [
            {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
            {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
        ]),
        ("CANCELED", [
            {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
            {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
        ]),
        ("PENDING", []),
    ]
)
def test_filter_by_state(transactions_fixture: List[dict], state: str, expected: List[dict]) -> None:
    """Тест функции сортировки по статусу транзакции"""
    assert filter_by_state(transactions_fixture, state) == expected


@pytest.mark.parametrize(
    "transactions_fixture, reverse, expected",
    [
        ([{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
          {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
          {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
          {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}], True, [
            {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
            {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
            {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
            {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
        ]),
        ([{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
          {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
          {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
          {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}], False, [
            {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
            {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
            {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
            {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}
        ])
    ]
)
def test_sort_by_date(transactions_fixture: List[dict], reverse: bool, expected: List[dict]) -> None:
    """Тест функции сортировки по дате"""
    assert sort_by_date(transactions_fixture, reverse) == expected


def test_sort_by_date_invalid_data() -> None:
    """Тест функции сортировки по дате с заведомо неверными данными"""
    with pytest.raises(ValueError):
        sort_by_date([{"invalid": "data"}])
