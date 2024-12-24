import os

from dotenv import load_dotenv
from src.logger import setup_logger

ENV_FILE = "../.env"
# Настраиваем логгер
logger = setup_logger(name="utils", log_file="logs/utils.log")

def get_or_create_api_key() -> str:
    """
    Получает API-ключ из .env файла или запрашивает у пользователя и сохраняет его.
    """
    from dotenv import load_dotenv
    import os

    load_dotenv()
    api_key = os.getenv("API_KEY")

    if not api_key:
        logger.warning("API-ключ отсутствует. Запрашиваем у пользователя.")
        api_key = input("Введите API-ключ: ").strip()
        with open(".env", "a") as env_file:
            env_file.write(f"\nAPI_KEY={api_key}")
        logger.info("API-ключ успешно сохранен в .env.")
    else:
        logger.info("API-ключ успешно загружен из .env.")

    return api_key
