import os
import pandas as pd
from src.reports import spending_by_category, spending_by_weekday, spending_by_workday
from src.main import load_transactions


def run_all():
    """
    Запускает все функции анализа транзакций и сохраняет результаты.
    """
    # Укажите путь к файлу с транзакциями
    file_path = "data/operations.xlsx"

    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден.")
        return

    transactions = load_transactions(file_path)

    # Введите дату для анализа
    date = "31.12.2021"  # Пример даты
    print(f"Используемая дата: {date}")

    # Анализ трат по категории
    try:
        print("Анализ трат по категории...")
        category = "каршеринг"  # Пример категории
        category_result = spending_by_category(transactions, category, date)
        if isinstance(category_result, str):
            print(category_result)
        else:
            print(category_result)
    except Exception as e:
        print(f"Ошибка при анализе трат по категории: {e}")

    # Анализ трат по дням недели
    try:
        print("Анализ трат по дням недели...")
        weekday_result = spending_by_weekday(transactions, date)
        weekday_result.columns = ["День недели", "Средние траты"]
        print(weekday_result)
    except Exception as e:
        print(f"Ошибка при анализе трат по дням недели: {e}")

    # Анализ трат в рабочие/выходные дни
    try:
        print("Анализ трат в рабочие/выходные дни...")
        workday_result = spending_by_workday(transactions, date)
        workday_result.columns = ["Рабочий день", "Средние траты"]
        print(workday_result)
    except Exception as e:
        print(f"Ошибка при анализе трат в рабочие/выходные дни: {e}")


if __name__ == "__main__":
    run_all()
