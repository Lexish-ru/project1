import re
from collections import Counter
from typing import Any, Dict, List

import pandas as pd

from src.logger import setup_logger

# Настраиваем логгер
logger = setup_logger(name="processing", log_file="logs/processing.log")


def filter_by_state(transactions: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Функция фильтрации транзакций по признаку 'STATE'"""
    valid_states = ["CANCELED", "EXECUTED", "PENDING"]
    state = state.upper()  # Приведение статуса к верхнему регистру
    if state not in valid_states:
        return []
    filtered_transactions = [
        transaction for transaction in transactions if transaction.get("state", "").upper() == state
    ]
    return filtered_transactions


import warnings


def sort_by_date(transactions: list, reverse: bool = False) -> list:
    """
    Функция сортировки по дате
    """
    valid_transactions = []
    for transaction in transactions:
        try:
            if "date" in transaction:
                transaction["date"] = pd.Timestamp(transaction["date"]).isoformat()
                valid_transactions.append(transaction)
            else:
                raise KeyError("Missing 'date' key")
        except Exception as e:
            warnings.warn(f"Некорректная дата в транзакции: {transaction}", UserWarning)
    return sorted(valid_transactions, key=lambda x: x["date"], reverse=reverse)


def search_transactions_by_regex(transactions: List[Dict], search_term: str) -> List[Dict]:
    """
    Ищет транзакции, где описание содержит заданную строку поиска.
    """
    pattern = re.compile(re.escape(search_term), re.IGNORECASE)
    return [transaction for transaction in transactions if pattern.search(transaction.get("description", ""))]


def count_transactions_by_category(transactions: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Считает количество операций для каждой категории из списка категорий.
    """
    category_counts = Counter()

    for transaction in transactions:
        description = transaction.get("description", "").lower()
        for category in categories:
            if category.lower() in description:
                category_counts[category] += 1

    return dict(category_counts)


def read_transactions_from_csv(file_path: str) -> List[Dict[str, str]]:
    """
    Считывает транзакции из CSV-файла.
    """
    try:
        data = pd.read_csv(file_path, sep=";", keep_default_na=False)

        data["amount"] = data["amount"].replace("", "0").astype(float)

        data["date"] = pd.to_datetime(data["date"], errors="coerce")

        data = data.dropna(subset=["date"])

        return data.to_dict(orient="records")
    except Exception as e:
        raise ValueError(f"Ошибка при чтении CSV-файла: {e}")


def read_transactions_from_excel(file_path: str) -> List[Dict[str, str]]:
    """Считывает транзакции из Excel-файла."""
    try:
        # Читаем данные из Excel
        data = pd.read_excel(file_path, engine="openpyxl", keep_default_na=False)
        return data.to_dict(orient="records")
    except Exception as e:
        raise ValueError(f"Ошибка при чтении Excel-файла: {e}")


def categorize_transactions_by_description(
    transactions: List[Dict[str, str]], categories: List[str]
) -> Dict[str, int]:
    """
    Подсчет категорий транзакций на основе описания.
    """
    category_counts = {category: 0 for category in categories}
    for transaction in transactions:
        description = transaction.get("description", "").lower()
        for category in categories:
            if category.lower() in description:
                category_counts[category] += 1
    return category_counts
