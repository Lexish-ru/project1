def get_mask_card_number(card_number: int) -> str:
    """Функция скытия номера карты введённого пользователем"""
    CARD_NUMBER_LEGHT = 16
    if len(card_number) == CARD_NUMBER_LEGHT and card_number.isdigit():
        masked_card_number = card_number[0:6] + "******" + card_number[-4:]
        return masked_card_number
    else:
        return "Введённые Вами данные не соответсвуют формату номера банковской карты"


def get_mask_account(bank_account: int, masked_account=None) -> str:
    """Функция, которая скрывает номер счёта введённого пользователем"""
    BANK_ACCOUNT_LEGHT = 20
    if len(bank_account) == BANK_ACCOUNT_LEGHT and bank_account.isdigit():
        masked_account = "**" + bank_account[-4:]
        return masked_account
    else:
        return "Введённые Вами данные не соответсвуют формату номера банковского счёта."
