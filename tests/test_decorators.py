import os

import pytest

from src.decorators import my_function

LOG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/mylog.txt"))


def test_my_function_sum() -> None:
    """Тест корректного суммирования двух чисел и создания лог-файла."""
    result = my_function(3, 4)
    assert result == 7, "Функция должна корректно складывать числа"

    # Проверяем, что лог-файл был создан
    assert os.path.exists(LOG_FILE), "Лог-файл должен быть создан в папке src"

    # Проверяем содержимое лог-файла
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

    # Проверяем, что логи содержат сообщение об ошибке
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
