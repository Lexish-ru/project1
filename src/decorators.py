import functools
import logging
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        logger = logging.getLogger(func.__name__)
        handler = logging.FileHandler(filename) if filename else logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                logger.info(f"{func.__name__} started with inputs: {args}, {kwargs}")
                result = func(*args, **kwargs)
                logger.info(f"{func.__name__} ok with result: {result}")
                return result
            except Exception as e:
                logger.error(f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}")
                raise
            finally:
                logger.info(f"{func.__name__} finished")

        return wrapper
    return decorator


@log(filename="mylog.txt")
def my_function(x: int, y: int) -> int:
    return x + y


if __name__ == "__main__":
    try:
        print(my_function(1, 2))
        print(my_function(1, "error"))  # This will raise a TypeError
    except Exception as e:
        print(f"Handled exception: {e}")
