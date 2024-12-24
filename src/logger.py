import logging
import os
from typing import Optional

# Создаем папку для логов, если она не существует
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger(name: str, log_file: str, level: int = logging.INFO) -> logging.Logger:
    """
    Настраивает логгер.

    Args:
        name (str): Название логгера.
        log_file (str): Путь до файла лога.
        level (int): Уровень логирования.

    Returns:
        logging.Logger: Настроенный логгер.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Создаем обработчик для записи в файл
    file_handler = logging.FileHandler(log_file, mode="w")  # Перезапись логов
    file_handler.setLevel(level)

    # Формат логирования
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    # Добавляем обработчик
    logger.addHandler(file_handler)

    return logger
