from unittest.mock import MagicMock, patch

from src.utils import save_to_file


@save_to_file("test_output.json")
def sample_function() -> dict:
    """Пример функции для тестирования декоратора."""
    return {"key": "value"}


@patch("builtins.open")
@patch("json.dump")
def test_save_to_file_mocked(mock_json_dump: MagicMock, mock_open: MagicMock) -> None:
    """Тестирует работу save_to_file с подменой записи в файл."""
    sample_function()
    # Проверяем, что файл открылся
    mock_open.assert_called_once()
    # Проверяем вызов json.dump
    mock_json_dump.assert_called_once_with({"key": "value"}, mock_open().__enter__(), indent=4, ensure_ascii=False)
