import os
from unittest.mock import mock_open, patch

from src.utils import get_or_create_api_key


@patch("builtins.input", return_value="test_api_key")
@patch("builtins.open", new_callable=mock_open)
@patch("os.getenv", side_effect=[None, "test_api_key"])
@patch("src.utils.load_dotenv")
def test_get_or_create_api_key_missing_key(mock_load_dotenv, mock_getenv, mock_open_file, mock_input):
    """Проверка: если ключ отсутствует, он запрашивается у пользователя и сохраняется."""
    api_key = get_or_create_api_key()
    assert api_key == "test_api_key"
    mock_open_file.assert_called_with(os.path.join(os.getcwd(), ".env"), "a", encoding="utf-8")
    mock_open_file().write.assert_called_with("API_KEY=test_api_key\n")


@patch("builtins.input", side_effect=["", "valid_api_key"])
@patch("builtins.open", new_callable=mock_open)
@patch("os.getenv", side_effect=[None, "valid_api_key"])
@patch("src.utils.load_dotenv")
def test_get_or_create_api_key_invalid_input(mock_load_dotenv, mock_getenv, mock_open_file, mock_input):
    """Проверка обработки пустого ввода API-ключа."""
    api_key = get_or_create_api_key()
    assert api_key == "valid_api_key"
    mock_open_file.assert_called_with(os.path.join(os.getcwd(), ".env"), "a", encoding="utf-8")
    mock_open_file().write.assert_called_with("API_KEY=valid_api_key\n")


@patch("os.getenv", return_value="existing_api_key")
@patch("src.utils.load_dotenv")
def test_get_or_create_api_key_existing_key(mock_load_dotenv, mock_getenv):
    """Проверка: если ключ существует, он возвращается из .env."""
    api_key = get_or_create_api_key()
    assert api_key == "existing_api_key"
