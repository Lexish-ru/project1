import logging
import os

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
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Удаляем старые обработчики, чтобы избежать дублирования
    if not any(isinstance(h, logging.FileHandler) and h.baseFilename == log_file for h in logger.handlers):
        file_handler = logging.FileHandler(log_file, mode="w")
        file_handler.setLevel(level)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
