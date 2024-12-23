import os

from dotenv import load_dotenv

ENV_FILE = ".env"


def get_or_create_api_key() -> str:
    """
    Получает API-ключ из .env файла или запрашивает у пользователя и сохраняет его.
    """
    load_dotenv()
    api_key = os.getenv("API_KEY")

    if not api_key:
        if os.environ.get("PYTEST_RUNNING"):  # Проверка, запущен ли pytest
            raise Exception("API-ключ не найден для тестов")
        if not api_key:
            while not api_key:
                api_key = input("Введите API-ключ: ").strip()
            with open(".env", "a") as env_file:
                env_file.write(f"\nAPI_KEY={api_key}")

    return api_key
