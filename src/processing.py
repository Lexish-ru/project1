from typing import Any, Dict, List


def filter_by_state(transactions: list[dict], state: str = 'EXECUTED') -> list[dict]:
    """Функция фильтрации транзакций по признаку 'STATE'"""
    if state not in ["CANCELED", "EXECUTED"]:
        return []
    filtered_transactions = [transaction for transaction in transactions if transaction.get("state") == state]
    return filtered_transactions


def sort_by_date(transactions: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """Функция сортировки по дате"""
    if not isinstance(transactions, list) or not all(isinstance(item, dict) for item in transactions):
        raise ValueError("Предоставленные данные не являются списком транзакций")
    for attribute in transactions:
        if not isinstance(attribute.get("date"), str):
            raise ValueError("Предоставленные данные не содержат даты")
    return sorted(transactions, key=lambda transaction: transaction.get("date", ""), reverse=reverse)
