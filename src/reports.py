import json
from typing import Optional, Callable
import pandas as pd
from datetime import datetime, timedelta


def save_to_file(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для сохранения результата функции в JSON-файл.

    :param filename: Имя файла, куда будет записан результат. Если None, будет использовано имя по умолчанию.
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            # Выполнение декорируемой функции
            result = func(*args, **kwargs)

            # Определяем имя файла
            output_file = filename or f"{func.__name__}_output.json"

            # Записываем результат в JSON-файл
            with open(output_file, "w", encoding="utf-8") as file:
                json.dump(result, file, indent=4, ensure_ascii=False)

            print(f"Результат функции '{func.__name__}' сохранен в файл: {output_file}")
            return result

        return wrapper

    return decorator


@save_to_file()
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> dict:
    """
    Рассчитывает траты по заданной категории за последние три месяца.

    :param transactions: DataFrame с транзакциями (должен содержать столбцы 'category', 'amount', 'date').
    :param category: Название категории.
    :param date: Опциональная дата (строка в формате 'YYYY-MM-DD'). Если не указана, берется текущая дата.
    :return: Словарь с итоговыми данными.
    """
    # Устанавливаем дату отсчета
    if date is None:
        current_date = datetime.now()
    else:
        current_date = datetime.strptime(date, '%Y-%m-%d')

    start_date = current_date - timedelta(days=90)

    # Преобразуем категории и даты
    transactions['category'] = transactions['category'].str.strip().str.lower()
    transactions['date'] = pd.to_datetime(transactions['date'], errors='coerce')

    # Вывод отладочной информации
    print(f"Все данные:\n{transactions[['date', 'category', 'amount']].head(20)}")

    # Фильтруем данные
    filtered_transactions = transactions[
        (transactions['date'] >= start_date) &
        (transactions['date'] <= current_date) &
        (transactions['category'] == category.lower())
        ]

    # Вывод после фильтрации
    print(f"Фильтрованные данные для категории '{category}':\n{filtered_transactions}")

    # Отладочная информация: вывод фильтрованных данных
    print(f"Фильтрованные данные для категории '{category}':\n{filtered_transactions}")

    # Суммируем траты
    total_spent = filtered_transactions['amount'].sum()

    # Формируем результат
    result = {
        "category": category,
        "total_spent": total_spent,
        "start_date": start_date.strftime('%Y-%m-%d'),
        "end_date": current_date.strftime('%Y-%m-%d'),
    }

    # Выводим сообщение, если данных нет
    if total_spent == 0.0:
        print(f"Для категории '{category}' не найдено данных за выбранный период.")

    return result


@save_to_file()
def spending_by_weekday(transactions: pd.DataFrame,
                        date: Optional[str] = None) -> dict:
    """
    Рассчитывает средние траты по дням недели за последние три месяца.

    :param transactions: DataFrame с транзакциями (должен содержать столбцы 'date' и 'amount').
    :param date: Опциональная дата (строка в формате 'YYYY-MM-DD'). Если не указана, берется текущая дата.
    :return: Словарь с данными по тратам в разрезе дней недели.
    """
    # Устанавливаем дату отсчета
    if date is None:
        current_date = datetime.now()
    else:
        current_date = datetime.strptime(date, '%Y-%m-%d')

    start_date = current_date - timedelta(days=90)

    # Фильтруем данные по дате
    filtered_transactions = transactions[
        (transactions['date'] >= start_date) &
        (transactions['date'] <= current_date)
        ]

    # Добавляем столбец с днем недели
    filtered_transactions['weekday'] = filtered_transactions['date'].dt.day_name()

    # Рассчитываем средние траты по дням недели
    average_spending = (
        filtered_transactions.groupby('weekday')['amount'].mean().sort_index()
    )

    # Преобразуем результат в словарь
    result = average_spending.to_dict()

    return {
        "start_date": start_date.strftime('%Y-%m-%d'),
        "end_date": current_date.strftime('%Y-%m-%d'),
        "average_spending_by_weekday": result
    }


@save_to_file()
def spending_by_workday(transactions: pd.DataFrame,
                        date: Optional[str] = None) -> dict:
    """
    Рассчитывает средние траты в рабочий и выходной день за последние три месяца.

    :param transactions: DataFrame с транзакциями (должен содержать столбцы 'date' и 'amount').
    :param date: Опциональная дата (строка в формате 'YYYY-MM-DD'). Если не указана, берется текущая дата.
    :return: Словарь с данными по средним тратам в рабочие и выходные дни.
    """
    # Устанавливаем дату отсчета
    if date is None:
        current_date = datetime.now()
    else:
        current_date = datetime.strptime(date, '%Y-%m-%d')

    start_date = current_date - timedelta(days=90)

    # Фильтруем данные по дате
    filtered_transactions = transactions[
        (transactions['date'] >= start_date) &
        (transactions['date'] <= current_date)
        ]

    # Добавляем столбец с признаком рабочего/выходного дня
    filtered_transactions['is_workday'] = filtered_transactions['date'].dt.weekday < 5  # True для рабочих дней

    # Рассчитываем средние траты для рабочих и выходных дней
    average_spending = (
        filtered_transactions.groupby('is_workday')['amount'].mean().to_dict()
    )

    # Формируем результат
    return {
        "start_date": start_date.strftime('%Y-%m-%d'),
        "end_date": current_date.strftime('%Y-%m-%d'),
        "average_spending": {
            "workday": average_spending.get(True, 0.0),
            "weekend": average_spending.get(False, 0.0)
        }
    }
