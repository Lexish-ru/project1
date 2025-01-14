import logging
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

from src.utils import save_to_file

# Настройка логгирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


@save_to_file()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> dict:
    """
    Рассчитывает траты по заданной категории за последние три месяца.
    """
    logging.info(f"Запуск функции spending_by_category с категорией: {category} и датой: {date}")

    if date is None:
        current_date = datetime.now()
    else:
        current_date = datetime.strptime(date, "%d.%m.%Y")
    start_date = current_date - timedelta(days=90)

    filtered_transactions = transactions[
        (transactions["date"] >= start_date)
        & (transactions["date"] <= current_date)
        & (transactions["category"].str.lower() == category.lower())
    ]

    total_spent = round(filtered_transactions["amount"].sum(), 2)
    logging.info(f"Суммарные траты по категории '{category}': {total_spent}")

    return {
        "category": category,
        "total_spent": total_spent,
        "start_date": start_date.strftime("%d.%m.%Y"),
        "end_date": current_date.strftime("%d.%m.%Y"),
    }


@save_to_file()
def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> dict:
    """
    Рассчитывает средние траты по дням недели за последние три месяца.
    """
    logging.info(f"Запуск функции spending_by_weekday с датой: {date}")

    if date is None:
        current_date = datetime.now()
    else:
        current_date = datetime.strptime(date, "%d.%m.%Y")
    start_date = current_date - timedelta(days=90)

    filtered_transactions = transactions[(transactions["date"] >= start_date) & (transactions["date"] <= current_date)]

    filtered_transactions = filtered_transactions.copy()
    filtered_transactions["weekday"] = filtered_transactions["date"].dt.day_name()

    average_spending = filtered_transactions.groupby("weekday")["amount"].mean().round(2).sort_index()

    logging.info(f"Средние траты по дням недели рассчитаны.")

    return {
        "start_date": start_date.strftime("%d.%m.%Y"),
        "end_date": current_date.strftime("%d.%m.%Y"),
        "average_spending_by_weekday": average_spending.to_dict(),
    }


@save_to_file()
def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> dict:
    """
    Рассчитывает средние траты в рабочий и выходной день за последние три месяца.
    """
    logging.info(f"Запуск функции spending_by_workday с датой: {date}")

    if date is None:
        current_date = datetime.now()
    else:
        current_date = datetime.strptime(date, "%d.%m.%Y")
    start_date = current_date - timedelta(days=90)

    filtered_transactions = transactions[(transactions["date"] >= start_date) & (transactions["date"] <= current_date)]

    filtered_transactions = filtered_transactions.copy()
    filtered_transactions["is_workday"] = filtered_transactions["date"].dt.weekday < 5

    average_spending = filtered_transactions.groupby("is_workday")["amount"].mean().round(2).to_dict()

    logging.info("Средние траты в рабочие и выходные дни рассчитаны.")

    return {
        "start_date": start_date.strftime("%d.%m.%Y"),
        "end_date": current_date.strftime("%d.%m.%Y"),
        "average_spending": {"workday": average_spending.get(True, 0.0), "weekend": average_spending.get(False, 0.0)},
    }
