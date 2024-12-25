
import os
from dotenv import load_dotenv

load_dotenv()

def get_or_create_api_key() -> str:
    """Получает API-ключ из файла .env или запрашивает у пользователя."""
    api_key = os.getenv("API_KEY")
    if not api_key:
        while not api_key:
            api_key = input("Введите API-ключ: ").strip()
            if not api_key:
                print("API-ключ не может быть пустым. Попробуйте снова.")

        # Save the API key to the .env file
        env_path = os.path.join(os.getcwd(), ".env")
        with open(env_path, "a", encoding="utf-8") as env_file:
            env_file.write(f"API_KEY={api_key}\n")
    
    return api_key
