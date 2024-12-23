import pytest
from src.utils import read_transactions
import json
from unittest.mock import mock_open, patch

# Тест: успешное чтение транзакций
def test_read_transactions_valid_file() -> None:
    valid_json = '[{"id": 1, "amount": 100.0}, {"id": 2, "amount": 200.0}]'
    with patch("builtins.open", mock_open(read_data=valid_json)):
        result = read_transactions("data/operations.json")
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == 1

# Тест: файл не найден
def test_read_transactions_file_not_found() -> None:
    result = read_transactions("data/nonexistent.json")
    assert result == []

# Тест: пустой файл
def test_read_transactions_empty_file() -> None:
    with patch("builtins.open", mock_open(read_data="")):
        result = read_transactions("data/operations.json")
        assert result == []

# Тест: некорректный формат данных
def test_read_transactions_invalid_format() -> None:
    invalid_json = '{"id": 1, "amount": 100.0}'  # JSON не является списком
    with patch("builtins.open", mock_open(read_data=invalid_json)):
        result = read_transactions("data/operations.json")
        assert result == []
