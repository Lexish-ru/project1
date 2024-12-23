from src.utils import read_transactions


def test_read_transactions_valid_file() -> None:
    data = read_transactions("data/operations.json")
    assert isinstance(data, list)


def test_read_transactions_invalid_file() -> None:
    data = read_transactions("data/nonexistent.json")
    assert data == []
