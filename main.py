import json
import os
from src.processing import (
    read_transactions_from_csv,
    read_transactions_from_excel,
    filter_by_state,
    sort_by_date,
    search_transactions_by_description,
)
from src.widget import get_date, mask_card_account


def format_transaction(transaction):
    """
    Форматирует транзакцию для вывода.
    :param transaction: Словарь с данными транзакции.
    :return: Отформатированная строка.
    """
    date = get_date(transaction.get("date", ""))
    description = transaction.get("description", "Нет описания")
    account_from = mask_card_account(transaction.get("from", ""))
    account_to = mask_card_account(transaction.get("to", ""))
    amount = transaction.get("amount", 0)
    currency = transaction.get("currency_name", "Unknown")

    return f"{date} {description}\n{account_from} -> {account_to}\nСумма: {amount} {currency}"


def main():
    """
    Основная функция программы для работы с банковскими транзакциями.
    """
    try:
        print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
        print("Выберите необходимый пункт меню:")
        print("1. Получить информацию о транзакциях из JSON-файла")
        print("2. Получить информацию о транзакциях из CSV-файла")
        print("3. Получить информацию о транзакциях из XLSX-файла")

        option = input("Ваш выбор: ").strip()
        file_type = {'1': 'json', '2': 'csv', '3': 'xlsx'}.get(option)

        if not file_type:
            raise ValueError("Некорректный выбор пункта меню.")

        print("Пожалуйста, поместите файл в папку 'data' в корне проекта.")
        file_name = input("Введите имя файла (с расширением): ").strip()
        file_path = os.path.join("data", file_name)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл '{file_name}' не найден в папке 'data'.")

        if file_type == 'json':
            with open(file_path, 'r', encoding='utf-8') as file:
                transactions = json.load(file)
        elif file_type == 'csv':
            transactions = read_transactions_from_csv(file_path)
        elif file_type == 'xlsx':
            transactions = read_transactions_from_excel(file_path)
        else:
            raise NotImplementedError(f"Обработка формата {file_type} не поддерживается.")

        print("Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")

        valid_statuses = {'executed', 'canceled', 'pending'}
        while True:
            status = input("Введите статус: ").strip().lower()
            if status in valid_statuses:
                filtered_transactions = filter_by_state(transactions, status)
                print(f"Операции отфильтрованы по статусу '{status.upper()}'.")
                print(f"Текущая выборка содержит {len(filtered_transactions)} операций.")
                break
            else:
                print(f'Статус операции "{status}" недоступен. Попробуйте снова.')

        sort_choice = input("Отсортировать операции по дате? Да/Нет: ").strip().lower()
        if sort_choice == 'да':
            while True:
                order = input("По возрастанию нажмите 1, по убыванию нажмите 2: ").strip()
                if order == '1':
                    reverse = False
                    break
                elif order == '2':
                    reverse = True
                    break
                else:
                    print("Некорректный выбор. Пожалуйста, выберите 1 или 2.")
            filtered_transactions = sort_by_date(filtered_transactions, reverse)
            print(f"Текущая выборка после сортировки содержит {len(filtered_transactions)} операций.")

        currency_choice = input("Выводить только рублевые транзакции? Да/Нет: ").strip().lower()
        if currency_choice == 'да':
            filtered_transactions = [t for t in filtered_transactions if 'руб' in t.get('currency_name', '').lower()]
            print(f"Текущая выборка после фильтрации по валюте содержит {len(filtered_transactions)} операций.")

        search_choice = input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет: ").strip().lower()
        if search_choice == 'да':
            search_word = input("Введите слово для поиска: ").strip()
            filtered_transactions = search_transactions_by_description(filtered_transactions, search_word)
            print(f"Текущая выборка после фильтрации по описанию содержит {len(filtered_transactions)} операций.")

        if not filtered_transactions:
            print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        else:
            print(f"Всего банковских операций в выборке: {len(filtered_transactions)}")
            for t in filtered_transactions:
                print(format_transaction(t))
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
