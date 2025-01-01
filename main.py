import json
import csv
from typing import List
from src.processing import (
    read_transactions_from_csv,
    read_transactions_from_excel,
    filter_by_state,
    sort_by_date,
    search_transactions_by_description,
)

def main():
    """
    Основная функция программы для работы с банковскими транзакциями.
    """
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Введите номер пункта меню: ").strip()

    if choice == "1":
        file_path = input("Введите путь к JSON-файлу: ").strip()
        with open(file_path, "r", encoding="utf-8") as f:
            transactions = json.load(f)
    elif choice == "2":
        file_path = input("Введите путь к CSV-файлу: ").strip()
        transactions = read_transactions_from_csv(file_path)
    elif choice == "3":
        file_path = input("Введите путь к XLSX-файлу: ").strip()
        transactions = read_transactions_from_excel(file_path)
    else:
        print("Некорректный выбор. Завершение работы.")
        return

    while True:
        status = input("Введите статус для фильтрации (EXECUTED, CANCELED, PENDING): ").strip().upper()
        if status not in {"EXECUTED", "CANCELED", "PENDING"}:
            print(f"Статус операции '{status}' недоступен.")
            continue
        transactions = filter_by_state(transactions, status)
        print(f"Операции отфильтрованы по статусу '{status}'.")
        break

    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    sort_choice = input("Отсортировать операции по дате? (Да/Нет): ").strip().lower()
    if sort_choice == "да":
        order = input("Сортировать по возрастанию или по убыванию? ").strip().lower()
        ascending = order == "по возрастанию"
        transactions = sort_by_date(transactions, ascending)

    currency_filter = input("Выводить только рублевые транзакции? (Да/Нет): ").strip().lower()
    if currency_filter == "да":
        transactions = [t for t in transactions if t.get("currency_name") == "RUB"]

    search_choice = input("Отфильтровать список транзакций по определенному слову в описании? (Да/Нет): ").strip().lower()
    if search_choice == "да":
        search_term = input("Введите слово для поиска: ").strip()
        transactions = search_transactions_by_description(transactions, search_term)

    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    print("Распечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(transactions)}")
    for transaction in transactions:
        print(transaction)

if __name__ == "__main__":
    main()
