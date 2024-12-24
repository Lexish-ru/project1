import logging
import os
import re

import pytest

from src.logger import setup_logger


@pytest.fixture
def temp_log_file(tmp_path):
    """
    Создает временный файл для логов.
    """
    log_file = tmp_path / "temp.log"
    return str(log_file)


@pytest.fixture
def logger_with_temp_file(temp_log_file):
    """
    Создает логгер, который пишет в временный файл.
    """
    logger = setup_logger("test_logger", temp_log_file, logging.DEBUG)
    yield logger
    # Удаляем обработчики после использования
    for handler in logger.handlers:
        logger.removeHandler(handler)


def test_logger_file_creation(temp_log_file, logger_with_temp_file):
    """
    Проверка, что файл логов создаётся.
    """
    logger = logger_with_temp_file
    logger.info("Тестовый лог")

    assert os.path.exists(temp_log_file), "Файл логов не создан."


def test_logger_log_format(temp_log_file, logger_with_temp_file):
    """
    Проверка формата записи логов.
    """
    logger = logger_with_temp_file
    logger.info("Тестовый лог")

    with open(temp_log_file, "r") as f:
        log_content = f.read()

    # Проверяем наличие ключевых элементов в логе
    assert "INFO" in log_content, "Уровень логирования не записан."
    assert "test_logger" in log_content, "Название логгера отсутствует."
    assert "Тестовый лог" in log_content, "Сообщение лога отсутствует."

    # Регулярное выражение для проверки формата времени
    timestamp_regex = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
    assert re.search(timestamp_regex, log_content), "Метка времени отсутствует."


def test_logger_levels(temp_log_file, logger_with_temp_file):
    """
    Проверка работы разных уровней логирования.
    """
    logger = logger_with_temp_file
    logger.debug("Debug сообщение")
    logger.info("Info сообщение")
    logger.warning("Warning сообщение")
    logger.error("Error сообщение")
    logger.critical("Critical сообщение")

    with open(temp_log_file, "r") as f:
        log_content = f.read()

    # Проверяем, что все уровни логов записаны
    assert "DEBUG" in log_content, "Debug уровень не записан."
    assert "INFO" in log_content, "Info уровень не записан."
    assert "WARNING" in log_content, "Warning уровень не записан."
    assert "ERROR" in log_content, "Error уровень не записан."
    assert "CRITICAL" in log_content, "Critical уровень не записан."


def test_logger_reuse(temp_log_file):
    """
    Проверка, что повторное использование логгера работает корректно.
    """
    logger1 = setup_logger("test_logger", temp_log_file, logging.INFO)
    logger1.info("Первый лог")

    # Повторный вызов setup_logger для того же логгера
    logger2 = setup_logger("test_logger", temp_log_file, logging.INFO)
    logger2.warning("Второй лог")

    with open(temp_log_file, "r") as f:
        log_content = f.read()

    # Проверяем, что оба лога записаны корректно
    assert "Первый лог" in log_content, "Первый лог не записан."
    assert "Второй лог" in log_content, "Второй лог не записан."


def test_logger_error_handling(temp_log_file):
    """
    Проверка обработки ошибок при записи в файл.
    """
    logger = setup_logger("test_logger", temp_log_file, logging.ERROR)
    logger.error("Error сообщение")

    # Убедимся, что файл логов был создан
    assert os.path.exists(temp_log_file), "Файл логов не создан."

    # Читаем содержимое файла логов
    with open(temp_log_file, "r") as f:
        log_content = f.read()

    assert "Error сообщение" in log_content, "Error сообщение не записано."

    # Проверяем, что другие уровни логов не записаны
    assert "INFO" not in log_content, "INFO уровень не должен быть записан."
