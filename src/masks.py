def get_mask_card_number(card_number: str) -> str:
    """Функция скытия номера карты введённого пользователем"""
    CARD_NUMBER_LEGHT = int(16)
    if CARD_NUMBER_LEGHT != len(card_number):
        return "Введённые Вами данные не соответсвуют формату номера банковской карты"
    else:
        if card_number.isdigit():
            masked_card_number = card_number[0:4] + " " + card_number[4:6] + "** **** " + card_number[-4:]
            return str(masked_card_number)
        else:
            return "Введённые Вами данные не соответсвуют формату номера банковской карты"


def get_mask_account(bank_account: str) -> str:
    """Функция, которая скрывает номер счёта введённого пользователем"""
    BANK_ACCOUNT_LEGHT = 20
    if len(bank_account) == BANK_ACCOUNT_LEGHT and bank_account.isdigit():
        masked_account = "**" + bank_account[-4:]
        return str(masked_account)
    else:
        return "Введённые Вами данные не соответсвуют формату номера банковского счёта."
