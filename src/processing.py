from typing import Any
from src.widget import get_date


def filter_by_state(info_line: list[list[dict]] | Any, state: Any='EXECUTED') -> list[list[dict]]:
    """Функиия сортивровки строк по признаку "STATE"""
    state_list = []
    for attribute in info_line:
        if attribute["state"] == state:
            state_list.append(attribute)
    return state_list


def sort_by_date(info_line: list[list[dict]] | Any, reverse: bool = True) -> list[list[dict]]:
    """функция сортировки по датам"""
    dates_list = []
    for i in info_line:
        converted_date = get_date(i['date'])
        dates_list.append(converted_date)
    return sorted(dates_list, reverse = reverse)
