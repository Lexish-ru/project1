from unittest.mock import MagicMock, patch

import requests

from src.external_api import convert_to_rub


@patch("src.external_api.get_or_create_api_key", return_value="mock_api_key")
@patch("src.external_api.requests.get")
def test_convert_to_rub_usd_to_rub(mock_requests_get: MagicMock, mock_get_api_key: MagicMock) -> None:
    """
    Проверка успешной конвертации из USD в рубли.
    """
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": 7500.0}
    mock_response.status_code = 200
    mock_requests_get.return_value = mock_response

    result = convert_to_rub(100, "USD")
    assert result == 7500.0
    mock_requests_get.assert_called_once()


@patch("src.external_api.get_or_create_api_key", return_value="mock_api_key")
def test_convert_to_rub_rub_to_rub(mock_get_api_key):
    """
    Проверка, что сумма в рублях остаётся неизменной.
    """
    result = convert_to_rub(100, "RUB")
    assert result == 100.0


@patch("src.external_api.get_or_create_api_key", return_value="mock_api_key")
@patch("src.external_api.requests.get")
def test_convert_to_rub_api_error(mock_requests_get: MagicMock, mock_get_api_key: MagicMock) -> None:
    ...
    """
    Проверка обработки ошибки API.
    """
    mock_requests_get.side_effect = requests.RequestException("API Error")
    result = convert_to_rub(100, "USD")
    assert result == 0.0
    mock_requests_get.assert_called_once()


@patch("src.external_api.get_or_create_api_key", return_value="mock_api_key")
@patch("src.external_api.requests.get")
def test_convert_to_rub_invalid_currency(mock_requests_get, mock_get_api_key):
    """
    Проверка, что некорректный код валюты возвращает 0.0.
    """
    mock_response = MagicMock()
    mock_response.json.return_value = {"error": "Invalid currency"}
    mock_response.status_code = 400
    mock_requests_get.return_value = mock_response

    result = convert_to_rub(100, "XYZ")
    assert result == 0.0
    mock_requests_get.assert_called_once()


@patch("src.external_api.get_or_create_api_key", return_value="mock_api_key")
@patch("src.external_api.requests.get")
def test_convert_to_rub_large_amount(mock_requests_get, mock_get_api_key):
    """
    Проверка конвертации крупной суммы.
    """
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": 7500000.0}
    mock_response.status_code = 200
    mock_requests_get.return_value = mock_response

    result = convert_to_rub(100000, "USD")
    assert result == 7500000.0
