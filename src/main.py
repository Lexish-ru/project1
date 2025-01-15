import os
import pandas as pd
from src.reports import spending_by_category, spending_by_weekday, spending_by_workday
from src.utils import save_to_file

def load_transactions(file_path: str) -> pd.DataFrame:
    """
    Загружает транзакции из файла и выполняет базовую обработку.
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    full_path = os.path.join(project_root, file_path)

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Файл {full_path} не найден.")

    transactions = pd.read_excel(full_path)

    # Переименовываем и форматируем данные
    transactions = transactions.rename(
        columns={"Дата операции": "date", "Категория": "category", "Сумма операции": "amount"}
    )

    # Преобразование даты
    transactions["date"] = pd.to_datetime(transactions["date"], format="%d.%m.%Y %H:%M:%S", errors="coerce")

    # Удаление пробелов и приведение категорий к нижнему регистру
    transactions["category"] = transactions["category"].str.strip().str.lower()

    # Проверка на некорректные даты
    if transactions["date"].isnull().any():
        invalid_dates = transactions[transactions["date"].isnull()]
        print("Некорректные строки с датами:", invalid_dates)
        raise ValueError("Некорректные значения в столбце 'date'. Проверьте данные.")

    return transactions


def main() -> None:
    """
    Основная функция программы.
    """
    print("Программа анализа транзакций")
    print("Выберите действие:")
    print("1. Траты по категории")
    print("2. Траты по дням недели")
    print("3. Траты в рабочий/выходной день")
    print("0. Выход")

    while True:
        choice = input("Введите номер действия: ")
        if choice == "0":
            print("Выход из программы.")
            break

        try:
            file_path = input("Введите путь к файлу с транзакциями (например, data/operations.xlsx): ")
            transactions = load_transactions(file_path)

            if choice == "1":
                category = input("Введите категорию: ")
                date = input("Введите дату (формат ДД.ММ.ГГГГ, оставьте пустым для текущей даты): ") or None
                result = spending_by_category(transactions, category, date)
                print("Результат анализа (траты по категории):")
                if isinstance(result, str):
                    print(result)
                else:
                    print(result)

            elif choice == "2":
                date = input("Введите дату (формат ДД.ММ.ГГГГ, оставьте пустым для текущей даты): ") or None
                result = spending_by_weekday(transactions, date)
                print("Результат анализа (средние траты по дням недели):")
                result.columns = ["День недели", "Средние траты"]
                print(result)

            elif choice == "3":
                date = input("Введите дату (формат ДД.ММ.ГГГГ, оставьте пустым для текущей даты): ") or None
                result = spending_by_workday(transactions, date)
                print("Результат анализа (средние траты в рабочие/выходные дни):")
                result.columns = ["Рабочий день", "Средние траты"]
                print(result)

            else:
                print("Неверный выбор. Попробуйте снова.")

        except Exception as e:
            print(f"Ошибка: {e}")
            continue

if __name__ == "__main__":
    main()
