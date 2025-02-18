import json
import os
from functools import wraps
from typing import Any, Callable, Optional

import pandas as pd


def save_to_file(filename: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Экспортирует результаты обработки транзакций в JSON файл
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)

            # Определяем корень проекта
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

            # Приведение пути filename к абсолютному
            if filename:
                if not os.path.isabs(filename):
                    output_path = os.path.normpath(os.path.join(project_root, filename))
                else:
                    output_path = filename
            else:
                output_file = f"{func.__name__}_output.json"
                output_path = os.path.join(project_root, "output", output_file)

            # Создаем директорию, если её нет
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Сохранение результата
            if isinstance(result, pd.DataFrame):
                result.to_json(output_path, orient="records", force_ascii=False, indent=4)
            else:
                with open(output_path, "w", encoding="utf-8") as file:
                    json.dump(result, file, indent=4, ensure_ascii=False)

            print(f"Результат функции '{func.__name__}' сохранен в файл: {output_path}")
            return result

        return wrapper

    return decorator
