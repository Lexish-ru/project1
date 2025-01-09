import logging
import os

import pytest

from src.decorators import log, my_function

# Лог-файл в корне проекта
LOG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mylog.txt"))


def test_my_function_sum() -> None:
    """Тест корректного суммирования двух чисел и создания лог-файла."""
    result = my_function(3, 4)
    assert result == 7, "Функция должна корректно складывать числа"
    assert os.path.exists(LOG_FILE), "Лог-файл должен быть создан в корне проекта"
    with open(LOG_FILE, "r") as f:
        logs = f.read()
        assert "Функция 'my_function' запущена" in logs
        assert "Функция 'my_function' выполнена" in logs


def test_my_function_type_error() -> None:
    """Тест обработки исключений при некорректных типах аргументов."""
    with pytest.raises(TypeError):
        my_function("a", "b")
    with open(LOG_FILE, "r") as f:
        logs = f.read()
    assert "Ошибка в функции 'my_function'" in logs


def test_my_function_zero() -> None:
    """Тест суммирования нулевых значений."""
    result = my_function(0, 0)
    assert result == 0


def test_log_file_creation() -> None:
    """Тест создания лог-файла при вызове функции с декоратором."""
    my_function(1, 1)
    assert os.path.exists(LOG_FILE)
    with open(LOG_FILE, "r") as f:
        logs = f.read()
        assert "Функция 'my_function' запущена" in logs
        assert "Функция 'my_function' выполнена" in logs


@log()
def sample_function(a, b):
    return a + b


@log()
def error_function():
    raise ValueError("Test Error")


def test_log_to_stream(caplog):
    """Тест логирования в поток через обработчик StreamHandler."""
    with caplog.at_level(logging.INFO, logger="sample_function"):
        result = sample_function(1, 2)
        assert result == 3

    # Проверяем захваченные логи
    captured_logs = [record.message for record in caplog.records]
    print(f"Captured logs: {captured_logs}")  # Отладочный вывод
    assert any("Функция 'sample_function' запущена" in log for log in captured_logs)
    assert any("Функция 'sample_function' выполнена" in log for log in captured_logs)


def test_log_error_handling(caplog):
    """Тест логирования ошибок."""
    with caplog.at_level(logging.ERROR, logger="error_function"):
        with pytest.raises(ValueError, match="Test Error"):
            error_function()

    # Проверяем захваченные логи
    captured_logs = [record.message for record in caplog.records]
    print(f"Captured logs: {captured_logs}")  # Отладочный вывод
    assert any("Ошибка в функции 'error_function'" in log for log in captured_logs)
    assert any("Test Error" in log for log in captured_logs)
