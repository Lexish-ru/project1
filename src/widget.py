import re

import pandas as pd

from src.logger import setup_logger
from src.masks import mask_bank_account, mask_card_number

# Настраиваем логгер
logger = setup_logger(name="widget", log_file="logs/widget.log")


def mask_card_account(number_import: str) -> str:
    """
    Функция обрабатывает номер карты и счёта.
    """
    # Выделяем числовую часть из строки
    number_match = re.search(r"\d+", number_import)
    if not number_match:
        logger.error(f"Некорректные данные: {number_import}")
        raise ValueError("Некорректные данные")

    number: str = number_match.group()

    if "Счет" in number_import:
        if not number.isdigit() or len(number) != 20:
            logger.error(f"Некорректный номер счёта: {number_import}")
            raise ValueError("Некорректный номер счета")
        return f"Cчёт {mask_bank_account(number)}"
    elif any(
        card_type in number_import for card_type in ["Visa", "Maestro", "Mastercard", "Discover", "American Express"]
    ):
        if not number.isdigit() or len(number) not in [15, 16]:
            logger.error(f"Некорректный номер карты: {number_import}")
            raise ValueError("Некорректный номер карты")
        card_mask: str = number_import.replace(number, mask_card_number(number))
        return card_mask
    else:
        logger.error(f"Некорректные данные: {number_import}")
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
