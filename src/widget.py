from src.masks import get_mask_account, get_mask_card_number


def mask_card_account(number_import: str) -> str:
    """"Функция обрабатывающая номер карты и счёта"""
    if 'Счет' in number_import:
        return f'Cчёт {get_mask_account(number_import[-20:])}'
    else:
        card_number = get_mask_card_number(number_import[-16:])
        card_mask = number_import.replace(number_import[-16:], card_number)
        return card_mask


def get_date(date: str) -> str:
    """Функция конвертации даты"""
    return f'{date[8:10]}.{date[5:7]}.{date[0:4]}'
