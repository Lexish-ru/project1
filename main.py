import json
import pandas as pd
from src.processing import (
    filter_by_state,
    sort_by_date,
    search_transactions_by_regex,
    count_transactions_by_category,
)
from src.masks import mask_card_number, mask_bank_account
from src.widget import get_date


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    while True:
        print("\nВыберите необходимый пункт меню:")
        print("1. Получить информацию о транзакциях из JSON-файла")
        print("2. Получить информацию о транзакциях из CSV-файла")
        print("3. Получить информацию о транзакциях из XLSX-файла")
        print("4. Выйти из программы")

        choice = input("Введите номер пункта меню: ").strip()

        if choice == "4":
            print("Спасибо за использование программы. До свидания!")
            break

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
                if t.get("currency_code", "").upper() in ruble_aliases or
                   t.get("currency_name", "").lower() in map(str.lower, ruble_aliases)
            ]

        print("\nРаспечатываю итоговый список транзакций:")
        for t in transactions:
            date_raw = t.get("date", "Неизвестно")
            try:
                date = pd.Timestamp(date_raw).strftime("%d.%m.%Y") if date_raw != "Неизвестно" else "Неизвестно"
            except Exception:
                date = "Неизвестно"

            description = t.get("description", "Неизвестно")
            amount = t.get("operationAmount", {}).get("amount", "Неизвестно")
            currency = t.get("operationAmount", {}).get("currency", {}).get("code", "Неизвестно")

            from_account = t.get("from", "").strip()
            to_account = t.get("to", "").strip()

            if "Счет" in from_account:
                from_account = f"Счет {mask_bank_account(from_account[-20:])}"
            elif from_account:
                from_account = mask_card_number(from_account[-16:])

            if "Счет" in to_account:
                to_account = f"Счет {mask_bank_account(to_account[-20:])}"
            elif to_account:
                to_account = mask_card_number(to_account[-16:])

            print(f"{date} {description}")
            if from_account and to_account:
                print(f"{from_account} -> {to_account}")
            elif from_account:
                print(from_account)
            elif to_account:
                print(to_account)
            print(f"Сумма: {amount} {currency}\n")

if __name__ == "__main__":
    main()
