import json
import os
from typing import Optional, Callable


def save_to_file(filename: Optional[str] = None) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # Определяем путь до папки 'output', начиная с корня проекта
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
            output_dir = os.path.join(project_root, "output")
            os.makedirs(output_dir, exist_ok=True)

            # Генерируем имя файла для сохранения
            output_file = os.path.join(output_dir, filename or f"{func.__name__}_output.json")

            # Сохраняем результат в файл
            with open(output_file, "w", encoding="utf-8") as file:
                json.dump(result, file, indent=4, ensure_ascii=False)

            print(f"Результат функции '{func.__name__}' сохранен в файл: {output_file}")
            return result

        return wrapper

    return decorator
