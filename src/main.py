import pandas as pd
from src.reports import spending_by_category, spending_by_weekday, spending_by_workday
import os

def load_transactions(file_path: str) -> pd.DataFrame:
    """
    Загружает транзакции из Excel-файла в DataFrame.1
    """
    # Определяем абсолютный путь к корню проекта
    project_root = os.path.abspath(os.path.dirname(__file__) + "/..")
    full_path = os.path.join(project_root, file_path)

    if not os.path.exists(full_path):
        print(f"Ожидаемый путь к файлу: {full_path}")
        raise FileNotFoundError(f"Файл {full_path} не найден.")

    transactions = pd.read_excel(full_path)

    # Проверяем наличие необходимых столбцов
    required_columns = {'Дата операции', 'Категория', 'Сумма операции'}
    if not required_columns.issubset(transactions.columns):
        raise ValueError(f"В файле отсутствуют необходимые столбцы: {required_columns - set(transactions.columns)}")

    # Переименовываем столбцы для унификации
    transactions = transactions.rename(columns={
        'Дата операции': 'date',
        'Категория': 'category',
        'Сумма операции': 'amount'
    })

    # Преобразуем столбец дат
    # Преобразуем столбец дат
    transactions['date'] = pd.to_datetime(
        transactions['date'], format='%d.%m.%Y %H:%M:%S', errors='coerce'
    )

    # Проверяем на наличие некорректных дат
    if transactions['date'].isnull().any():
        invalid_dates = transactions[transactions['date'].isnull()]
        print("Некорректные значения в столбце 'date':")
        print(invalid_dates)
        raise ValueError("В столбце 'date' обнаружены некорректные значения. Проверьте данные в файле.")

    return transactions



def main():
    """
    Основной интерфейс приложения.
    Позволяет пользователю выбрать действие и выполнить анализ транзакций.
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

        file_path = input("Введите путь к файлу с транзакциями (например, data/operations.xlsx): ")
        while True:
            try:
                transactions = load_transactions(file_path)
                break
            except FileNotFoundError as e:
                print(f"Ошибка загрузки файла: {e}")
                file_path = input("Попробуйте снова ввести путь к файлу с транзакциями: ")

        if choice == "1":
            print(
                f"Доступные данные: с {transactions['date'].min().strftime('%d.%m.%Y')} по {transactions['date'].max().strftime('%d.%m.%Y')}")
            category = input("Введите категорию: ")
            date = input("Введите дату (формат ДД.ММ.ГГГГ, оставьте пустым для текущей даты): ")
            date = date if date else None
            result = spending_by_category(transactions, category, date)
            print("Результат анализа:", result)

        elif choice == "2":
            print(
                f"Доступные данные: с {transactions['date'].min().strftime('%d.%m.%Y')} по {transactions['date'].max().strftime('%d.%m.%Y')}")
            date = input("Введите дату (формат ДД.ММ.ГГГГ, оставьте пустым для текущей даты): ")
            date = date if date else None
            result = spending_by_weekday(transactions, date)
            print("Результат анализа:", result)

        elif choice == "3":
            print(
                f"Доступные данные: с {transactions['date'].min().strftime('%d.%m.%Y')} по {transactions['date'].max().strftime('%d.%m.%Y')}")
            date = input("Введите дату (формат ДД.ММ.ГГГГ, оставьте пустым для текущей даты): ")
            date = date if date else None
            result = spending_by_workday(transactions, date)
            print("Результат анализа:", result)

        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
