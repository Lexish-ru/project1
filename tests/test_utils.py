from unittest.mock import mock_open, patch

from src.utils import get_or_create_api_key


@patch("builtins.input", return_value="test_api_key")
@patch("builtins.open", new_callable=mock_open)
@patch("os.getenv", return_value=None)
@patch("src.utils.load_dotenv")
def test_get_or_create_api_key_missing_key(mock_load_dotenv, mock_getenv, mock_open_file, mock_input):
    """
    Проверка, что функция запрашивает API-ключ у пользователя, если ключ отсутствует,
    и сохраняет его в .env.
    """
    api_key = get_or_create_api_key()

    assert api_key == "test_api_key"
    mock_input.assert_called_once_with("Введите API-ключ: ")
    mock_open_file.assert_called_once_with("../.env", "a")
    mock_open_file().write.assert_called_once_with("\nAPI_KEY=test_api_key")


@patch("os.getenv", return_value="existing_api_key")
@patch("src.utils.load_dotenv")
def test_get_or_create_api_key_existing_key(mock_load_dotenv, mock_getenv):
    """
    Проверка, что функция возвращает существующий API-ключ из переменных окружения.
    """
    api_key = get_or_create_api_key()
    assert api_key == "existing_api_key"
    mock_getenv.assert_called_once_with("API_KEY")


@patch("builtins.input", side_effect=["", "valid_api_key"])
@patch("builtins.open", new_callable=mock_open)
@patch("os.getenv", return_value=None)
@patch("src.utils.load_dotenv")
def test_get_or_create_api_key_invalid_input(mock_load_dotenv, mock_getenv, mock_open_file, mock_input):
    """
    Проверка обработки случая, когда пользователь вводит пустую строку вместо API-ключа.
    """
    api_key = get_or_create_api_key()

    assert api_key == "valid_api_key"
    assert mock_input.call_count == 2
    mock_open_file.assert_called_once_with("../.env", "a")
    mock_open_file().write.assert_called_once_with("\nAPI_KEY=valid_api_key")
