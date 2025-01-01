import logging
import os
from functools import wraps
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Декоратор для логирования выполнения функции.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger = logging.getLogger(func.__name__)
            logger.setLevel(logging.INFO)

            if logger.hasHandlers():
                logger.handlers.clear()

            if filename:
                base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
                os.makedirs(base_dir, exist_ok=True)
                abs_path = os.path.join(base_dir, filename)

                file_handler = logging.FileHandler(abs_path, mode="a")
                formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
            else:
                stream_handler = logging.StreamHandler()
                logger.addHandler(stream_handler)

            try:
                logger.info(f"Функция '{func.__name__}' запущена с аргументами: {args}, {kwargs}")
                result = func(*args, **kwargs)
                logger.info(f"Функция '{func.__name__}' выполнена. Результат: {result}")
                return result
            except Exception as e:
                logger.error(f"Ошибка в функции '{func.__name__}': {e}")
                raise

        return wrapper

    return decorator


@log(filename="mylog.txt")
def my_function(x: int, y: int) -> int:
    """Функция для суммирования двух чисел."""
    if not isinstance(x, int) or not isinstance(y, int):
        raise TypeError("Аргументы должны быть целыми числами")
    return x + y


if __name__ == "__main__":
    """Точка входа для выполнения кода."""
    try:
        print(my_function(1, 2))  # Выводит сумму 1 и 2
        print(my_function("a", "b"))  # Провоцирует ошибку
    except Exception as e:
        print(f"Получено исключение: {e}")
