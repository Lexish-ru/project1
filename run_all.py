import os

import pandas as pd

from src.reports import spending_by_category, spending_by_weekday, spending_by_workday

# Путь к файлу транзакций
TRANSACTIONS_FILE = "data/operations.xlsx"

# Проверка существования файла
if not os.path.exists(TRANSACTIONS_FILE):
    print(f"Файл {TRANSACTIONS_FILE} не найден. Убедитесь, что указали правильный путь.")
    exit(1)


# Загрузка транзакций
def load_transactions(file_path: str) -> pd.DataFrame:
    """Загружает данные из файла транзакций."""
    try:
        transactions = pd.read_excel(file_path)
        transactions["date"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")
        transactions["category"] = transactions["Категория"].str.lower()
        transactions["amount"] = transactions["Сумма операции"]
        return transactions
    except Exception as e:
        print(f"Ошибка при загрузке файла транзакций: {e}")
        exit(1)


# Основная функция
def run_all() -> None:
    """Запускает все функциональности проекта."""
    transactions = load_transactions(TRANSACTIONS_FILE)

    # Пример использования всех функций
    print("\n--- Траты по категории ---")
    spending_by_category(transactions, category="каршеринг", date="30.12.2021")

    print("\n--- Траты по дням недели ---")
    spending_by_weekday(transactions, date="30.12.2021")

    print("\n--- Траты в рабочий/выходной день ---")
    spending_by_workday(transactions, date="30.12.2021")


if __name__ == "__main__":
    run_all()
