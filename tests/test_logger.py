import os


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


def test_logger_levels(temp_log_file, logger_with_temp_file):
    """
    Проверка работы разных уровней логирования.
    """
    logger = logger_with_temp_file
    logger.debug("Debug сообщение")
    logger.info("Info сообщение")
    logger.warning("Warning сообщение")
    logger.error("Error сообщение")

    with open(temp_log_file, "r") as f:
        log_content = f.read()

    # Проверяем, что все уровни логов записаны
    assert "DEBUG" in log_content, "Debug уровень не записан."
    assert "INFO" in log_content, "Info уровень не записан."
    assert "WARNING" in log_content, "Warning уровень не записан."
    assert "ERROR" in log_content, "Error уровень не записан."
