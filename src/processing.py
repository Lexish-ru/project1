from typing import Any, Dict, List

import re

import pandas as pd


def filter_by_state(transactions: list[dict], state: str = "EXECUTED") -> list[dict]:
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
    """Считывает транзакции из Excel-файла.

    :param file_path: Путь к файлу Excel.
    :return: Список транзакций в виде словарей.
    """
    try:
        # Читаем данные из Excel
        data = pd.read_excel(file_path, engine="openpyxl", keep_default_na=False)
        return data.to_dict(orient="records")
    except Exception as e:
        raise ValueError(f"Ошибка при чтении Excel-файла: {e}")


def search_transactions_by_description(transactions: List[Dict[str, str]], search_term: str) -> List[Dict[str, str]]:
    """
    Поиск транзакций по строке в описании.

    :param transactions: Список словарей с данными о транзакциях.
    :param search_term: Строка для поиска в описании транзакций.
    :return: Список транзакций, содержащих строку поиска в поле description.
    """
    pattern = re.compile(re.escape(search_term), re.IGNORECASE)
    return [transaction for transaction in transactions if pattern.search(transaction.get('description', ''))]

def categorize_transactions_by_description(transactions: List[Dict[str, str]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчет категорий транзакций на основе описания.

    :param transactions: Список словарей с данными о транзакциях.
    :param categories: Список категорий для подсчета.
    :return: Словарь, где ключи - категории, а значения - количество транзакций в каждой категории.
    """
    category_counts = {category: 0 for category in categories}
    for transaction in transactions:
        description = transaction.get('description', '').lower()
        for category in categories:
            if category.lower() in description:
                category_counts[category] += 1
    return category_counts

