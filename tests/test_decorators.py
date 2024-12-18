import pytest

from src.decorators import log


@log()
def test_function_success(a: int, b: int) -> int:
    return a * b


@log()
def test_function_failure(a: int, b: int) -> float:
    return a / b


def test_log_success_file(mock_file_log):
    # Применяем декоратор с указанием файла
    decorated_test_func = log(filename=str(mock_file_log))(test_function_success)
    result = decorated_test_func(4, 5)  # Передаем параметры напрямую
    assert result == 20
    with open(mock_file_log, "r") as log_file:
        log_content = log_file.read()
        assert "test_function_success started with inputs" in log_content
        assert "test_function_success ok with result" in log_content


def test_log_failure_file(mock_file_log):
    # Применяем декоратор с указанием файла
    decorated_test_func = log(filename=str(mock_file_log))(test_function_failure)
    with pytest.raises(ZeroDivisionError):
        decorated_test_func(1, 0)  # Передаем параметры напрямую
    with open(mock_file_log, "r") as log_file:
        log_content = log_file.read()
        assert "test_function_failure error: ZeroDivisionError" in log_content
        assert "Inputs: (1, 0), {}" in log_content
