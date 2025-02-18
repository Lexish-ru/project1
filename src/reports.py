import logging
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

from src.utils import save_to_file


@save_to_file()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Рассчитывает траты по заданной категории за последние три месяца.
    """
    if date is None:
        current_date = pd.Timestamp.now()
    else:
        current_date = pd.to_datetime(date, dayfirst=True, format="%d.%m.%Y")
    start_date = current_date - pd.Timedelta(days=90)

    # Нормализуем данные перед фильтрацией
    transactions["category"] = transactions["category"].str.strip().str.lower()
    category = category.strip().lower()

    filtered_transactions = transactions[
        (transactions["date"] >= start_date)
        & (transactions["date"] <= current_date)
        & (transactions["category"] == category)
    ]

    if filtered_transactions.empty:
        return "Нет трат по данной категории в выбранный период."

    total_spent = filtered_transactions["amount"].sum()
    result = pd.DataFrame(
        [
            {
                "Категория": category,
                "Общая сумма трат": total_spent,
                "Начальная дата": start_date.strftime("%d.%m.%Y"),
                "Конечная дата": current_date.strftime("%d.%m.%Y"),
            }
        ]
    )
    return result


@save_to_file()
def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """
    Рассчитывает средние траты по дням недели за последние три месяца.
    Возвращает результат в формате DataFrame.
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

    average_spending = (
        filtered_transactions.groupby("weekday")["amount"]
        .mean()
        .round(2)
        .reset_index()
        .rename(columns={"weekday": "day_of_week", "amount": "average_spending"})
    )

    logging.info(f"Средние траты по дням недели рассчитаны.")
    return average_spending


@save_to_file()
def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """
    Рассчитывает средние траты в рабочий и выходной день за последние три месяца.
    Возвращает результат в формате DataFrame.
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

    average_spending = (
        filtered_transactions.groupby("is_workday")["amount"]
        .mean()
        .round(2)
        .reset_index()
        .rename(columns={"is_workday": "workday", "amount": "average_spending"})
    )

    logging.info("Средние траты в рабочие и выходные дни рассчитаны.")
    return average_spending
