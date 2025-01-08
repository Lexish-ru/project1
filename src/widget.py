from src.masks import mask_bank_account, mask_card_number
import pandas as pd


def mask_card_account(number_import: str) -> str:
    """ "Функция обрабатывающая номер карты и счёта"""
    if "Счет" in number_import:
        account_number = number_import[-20:]
        if not account_number.isdigit() or len(account_number) != 20:
            raise ValueError("Некорректный номер счета")
        return f"Cчёт {mask_bank_account(account_number)}"
    elif any(card_type in number_import for card_type in ["Visa", "Maestro", "Mastercard"]):
        card_number = number_import[-16:]
        if not card_number.isdigit() or len(card_number) != 16:
            raise ValueError("Некорректный номер карты")
        card_mask = number_import.replace(card_number, mask_card_number(card_number))
        return card_mask
    else:
        raise ValueError("Некорректные данные")


def get_date(date: str | pd.Timestamp | None) -> str:
    """Функция конвертации даты"""
    if date is None:
        return "Неизвестно"
    if isinstance(date, pd.Timestamp):
        return date.strftime("%d.%m.%Y")
    if not isinstance(date, str) or len(date) < 10:
        return "Неизвестно"
    try:
        # Попытка распознать дату через pandas
        parsed_date = pd.Timestamp(date)
        return parsed_date.strftime("%d.%m.%Y")  # Возвращаем только дату
    except (ValueError, TypeError):
        # Если дата некорректная или неподдерживаемая
        return "Неизвестно"


