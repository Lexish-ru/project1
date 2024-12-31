import os

import pytest

from src.decorators import my_function

LOG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/mylog.txt"))


def test_my_function_sum() -> None:
    """Тест корректного суммирования двух чисел и создания лог-файла."""
    result = my_function(3, 4)
    assert result == 7, "Функция должна корректно складывать числа"
    assert os.path.exists(LOG_FILE), "Лог-файл должен быть создан в папке src"
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
    assert "Ошибка в функции 'my_function'" in logs, "Логи должны содержать запись об ошибке"
    assert "Аргументы должны быть целыми числами" in logs, "Логи должны указывать на причину ошибки"


def test_my_function_zero() -> None:
    """Тест суммирования нулевых значений."""
    result = my_function(0, 0)
    assert result == 0, "Сумма нулей должна быть равна 0"


def test_log_file_creation() -> None:
    """Тест создания лог-файла при вызове функции с декоратором."""
    my_function(1, 1)
    assert os.path.exists(LOG_FILE), "Лог-файл должен быть создан"
    with open(LOG_FILE, "r") as f:
        logs = f.read()
        assert "Функция 'my_function' запущена" in logs, "Логи должны содержать запись о запуске функции"
        assert "Функция 'my_function' выполнена" in logs, "Логи должны содержать запись об упешном выполнении функции"


import pytest
from unittest.mock import patch
from src.decorators import log

@log()
def sample_function(a, b):
    return a + b

@log()
def error_function():
    raise ValueError("Test Error")

def test_log_to_stream():
    """Test logging to stream handler when no filename is provided."""
    with patch("sys.stdout") as mock_stdout:
        result = sample_function(1, 2)
        assert result == 3
        assert "Функция 'sample_function' запущена" in mock_stdout.getvalue()
        assert "Функция 'sample_function' выполнена" in mock_stdout.getvalue()

def test_log_error_handling():
    """Test logging an error when the function raises an exception."""
    with patch("sys.stdout") as mock_stdout:
        with pytest.raises(ValueError, match="Test Error"):
            error_function()
        assert "Ошибка в функции 'error_function'" in mock_stdout.getvalue()
        assert "Test Error" in mock_stdout.getvalue()

def test_log_file_unwritable(tmp_path):
    """Test behavior when the log file is not writable."""
    unwritable_file = tmp_path / "unwritable.log"
    unwritable_file.touch(0o000)  # Create a file with no permissions

    @log(filename=str(unwritable_file))
    def sample_unwritable_function():
        return "Unwritable"

    with pytest.raises(PermissionError):
        sample_unwritable_function()


import pytest
from src.decorators import log

@log()
def sample_function(a, b):
    return a + b

@log()
def error_function():
    raise ValueError("Test Error")

def test_log_to_stream(caplog):
    """Test logging to stream handler when no filename is provided."""
    with caplog.at_level("INFO"):
        result = sample_function(1, 2)
        assert result == 3
        assert "Функция 'sample_function' запущена" in caplog.text
        assert "Функция 'sample_function' выполнена" in caplog.text

def test_log_error_handling(caplog):
    """Test logging an error when the function raises an exception."""
    with caplog.at_level("ERROR"):
        with pytest.raises(ValueError, match="Test Error"):
            error_function()
        assert "Ошибка в функции 'error_function'" in caplog.text
        assert "Test Error" in caplog.text
