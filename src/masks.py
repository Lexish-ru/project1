from src.logger import setup_logger

# Настраиваем логгер
logger = setup_logger(name="masks", log_file="logs/masks.log")


def mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты, оставляя первые 4, последние 4 цифры и две после первых 4 видимыми.
    """
    CARD_NUMBER_LENGTH = 16

    if len(card_number) != CARD_NUMBER_LENGTH or not card_number.isdigit():
        logger.error(f"Ошибка: некорректный номер карты: {card_number}")
        raise ValueError("Неверный формат номера банковской карты")

    masked_card = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    logger.info(f"Маскированный номер карты: {masked_card}")
    return masked_card


def mask_bank_account(bank_account: str) -> str:
    """
    Маскирует номер банковского счета, оставляя только последние 4 цифры видимыми.
    """
    BANK_ACCOUNT_LENGTH = 20

    if not bank_account or len(bank_account) != BANK_ACCOUNT_LENGTH or not bank_account.isdigit():
        logger.warning(f"Некорректный номер банковского счета: {bank_account}")
        return "Некорректный счет"

    masked_account = f"**{bank_account[-4:]}"
    logger.info(f"Маскированный номер счета: {masked_account}")
    return masked_account