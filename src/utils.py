import json
import os
import pandas as pd
from functools import wraps
from typing import Any, Callable, Optional


def save_to_file(filename: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            output_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../output")
            os.makedirs(output_dir, exist_ok=True)
            output_file = filename or f"{func.__name__}_output.json"
            output_path = os.path.join(output_dir, output_file)

            # Сохраняем результат
            if isinstance(result, pd.DataFrame):
                result.to_json(output_path, orient="records", force_ascii=False, indent=4)
            else:
                with open(output_path, "w", encoding="utf-8") as file:
                    json.dump(result, file, indent=4, ensure_ascii=False)

            print(f"Результат функции '{func.__name__}' сохранен в файл: {output_path}")
            return result

        return wrapper

    return decorator

