from src.masks import mask_bank_account, mask_card_number


def mask_card_account(number_import: str) -> str:
    """"Функция обрабатывающая номер карты и счёта"""
    if 'Счет' in number_import:
        account_number = number_import[-20:]
        if not account_number.isdigit() or len(account_number) != 20:
            raise ValueError("Некорректный номер счета")
        return f'Cчёт {mask_bank_account(account_number)}'
    elif any(card_type in number_import for card_type in ["Visa", "Maestro", "Mastercard"]):
        card_number = number_import[-16:]
        if not card_number.isdigit() or len(card_number) != 16:
            raise ValueError("Некорректный номер карты")
        card_mask = number_import.replace(card_number, mask_card_number(card_number))
        return card_mask
    else:
        raise ValueError("Некорректные данные")


def get_date(date: str) -> str:
    """Функция конвертации даты"""
    if not isinstance(date, str) or len(date) < 10:
        raise ValueError("Некорректная дата")
    try:
        year = int(date[0:4])
        month = int(date[5:7])
        day = int(date[8:10])
        if not (1 <= month <= 12 and 1 <= day <= 31):
            raise ValueError("Некорректная дата")
        return f'{day:02}.{month:02}.{year}'
    except (ValueError, IndexError, TypeError):
        raise ValueError("Некорректная дата")
