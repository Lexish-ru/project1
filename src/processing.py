from typing import Any, Dict, List

import re

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
    filtered_transactions = [transaction for transaction in transactions if transaction.get("state", "").upper() == state]
    return filtered_transactions


def sort_by_date(transactions: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Функция сортировки транзакций по дате.
    """
    valid_transactions = []
    invalid_transactions = []

    for transaction in transactions:
        date = transaction.get("date")
        if isinstance(date, str) and date:
            valid_transactions.append(transaction)
        else:
            logger.warning(f"Некорректная дата в транзакции: {transaction}")
            invalid_transactions.append(transaction)

    sorted_transactions = sorted(valid_transactions, key=lambda t: t["date"], reverse=reverse)

    if invalid_transactions:
        logger.warning(f"Всего {len(invalid_transactions)} транзакций пропущено из-за некорректной даты.")

    return sorted_transactions


def search_transactions_by_description(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """Функция поиска транзакций по описанию"""
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    return [transaction for transaction in transactions if pattern.search(transaction.get("description", ""))]


def read_transactions_from_csv(file_path: str) -> List[Dict[str, str]]:
    """Считывает транзакции из CSV-файла.

    :param file_path: Путь к файлу CSV.
    :return: Список транзакций в виде словарей.
    """
    try:
        data = pd.read_csv(file_path, sep=";", keep_default_na=False)

        # Заменяем пустые строки на 0 в колонке amount
        data["amount"] = data["amount"].replace("", "0").astype(float)

        # Преобразуем дату в формат datetime
        data["date"] = pd.to_datetime(data["date"], errors="coerce")

        # Удаляем строки с некорректными датами
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


def categorize_transactions_by_description(transactions: List[Dict[str, str]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчет категорий транзакций на основе описания."""
    category_counts = {category: 0 for category in categories}
    for transaction in transactions:
        description = transaction.get('description', '').lower()
        for category in categories:
            if category.lower() in description:
                category_counts[category] += 1
    return category_counts

