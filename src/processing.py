from typing import Any


def filter_by_state(transactions: list[dict] | Any, state: Any = 'EXECUTED') -> list[dict]:
    """Функиия сортивровки строк по признаку "STATE"""
    filtered_transactions = []
    for attribute in transactions:
        if attribute["state"] == state:
            filtered_transactions.append(attribute)
    return filtered_transactions


def sort_by_date(transactions: list[dict] | Any, reverse: bool = True) -> list[dict]:
    """функция сортировки по датам"""
    list_by_date = sorted(transactions, key=lambda dates_dict: dates_dict.get('date'), reverse=reverse)

    return list_by_date
