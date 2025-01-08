import json
import pandas as pd
from src.processing import (
    filter_by_state,
    sort_by_date,
    search_transactions_by_regex,
    count_transactions_by_category,
)
from src.widget import get_date, mask_card_account


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    while True:
        print("\nВыберите необходимый пункт меню:")
        print("1. Получить информацию о транзакциях из JSON-файла")
        print("2. Получить информацию о транзакциях из CSV-файла")
        print("3. Получить информацию о транзакциях из XLSX-файла")

        choice = input("Введите номер пункта меню: ").strip()

        if choice not in ["1", "2", "3"]:
            print("Некорректный выбор. Попробуйте снова.")
            continue

        file_path = input("Введите путь к файлу с транзакциями: ").strip()

        try:
            if choice == "1":
                with open(file_path, "r", encoding="utf-8") as f:
                    transactions = json.load(f)
            elif choice == "2":
                transactions = pd.read_csv(file_path, sep=";", keep_default_na=False).to_dict(orient="records")
            elif choice == "3":
                transactions = pd.read_excel(file_path, engine="openpyxl", keep_default_na=False).to_dict(orient="records")
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            continue

        while True:
            print("\nВведите статус, по которому необходимо выполнить фильтрацию.\nДоступные статусы: EXECUTED, CANCELED, PENDING")
            status = input("Статус: ").strip().upper()

            if status not in ["EXECUTED", "CANCELED", "PENDING"]:
                print(f"Статус операции \"{status}\" недоступен. Попробуйте снова.")
                continue

            transactions = filter_by_state(transactions, status)
            print(f"Операции отфильтрованы по статусу \"{status}\".")
            break

        if not transactions:
            print("Не найдено ни одной транзакции, подходящей под условия фильтрации.")
            continue

        print("\nОтсортировать операции по дате? Да/Нет")
        if input().strip().lower() == "да":
            print("Отсортировать по возрастанию или по убыванию? (введите: по возрастанию/по убыванию)")
            order = input().strip().lower()
            reverse = order == "по убыванию"
            transactions = sort_by_date(transactions, reverse=reverse)

        print("\nВыводить только рублевые транзакции? Да/Нет")
        if input().strip().lower() == "да":
            ruble_aliases = {"RUB", "руб.", "ruble"}
            transactions = [
                t for t in transactions
                if (
                        t.get("operationAmount", {}).get("currency", {}).get("code", "").lower() in map(str.lower,
                                                                                                        ruble_aliases)
                        or t.get("operationAmount", {}).get("currency", {}).get("name", "").lower() in map(str.lower,
                                                                                                           ruble_aliases)
                        or t.get("currency_code", "").upper() in ruble_aliases
                        or t.get("currency_name", "").lower() in map(str.lower, ruble_aliases)
                )
            ]

        print("\nРаспечатываю итоговый список транзакций:")
        for t in transactions:
            date = get_date(t.get("date", "Неизвестно"))
            description = t.get("description", "Неизвестно")
            amount = (
                t.get("operationAmount", {}).get("amount", "Неизвестно")
                if "operationAmount" in t
                else t.get("amount", "Неизвестно")
            )
            currency = (
                t.get("operationAmount", {}).get("currency", {}).get("code", "Неизвестно")
                if "operationAmount" in t
                else t.get("currency_code", "Неизвестно")
            )

            from_account = t.get("from", "Неизвестно").strip()
            to_account = t.get("to", "Неизвестно").strip()

            # Маскируем данные через функцию mask_card_account
            try:
                masked_from_account = mask_card_account(from_account)
            except ValueError:
                masked_from_account = "Некорректные данные"

            try:
                masked_to_account = mask_card_account(to_account)
            except ValueError:
                masked_to_account = "Некорректные данные"

            # Вывод транзакции
            print(f"{date} {description}")
            print(f"{masked_from_account} -> {masked_to_account}")
            print(f"Сумма: {amount} {currency}\n")


if __name__ == "__main__":
    main()
