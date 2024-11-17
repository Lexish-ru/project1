from src.masks import get_mask_account, get_mask_card_number

CARD_NUMBER = "7000792289606361"
BANK_ACCOUNT = "73654108430135874305"

print(f"Ваш номер банковской карты скрыт в целях конфиденциальности {get_mask_card_number(CARD_NUMBER)}")
print(f"Ваш номер лицевого счёта скрыт в целях конфиденциальности {get_mask_account(BANK_ACCOUNT)}")
