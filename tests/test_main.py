from unittest.mock import patch

import pandas as pd

from src.main import load_transactions, main


@patch("src.main.pd.read_excel")
def test_load_transactions(mock_read_excel, sample_transactions_file):
    """
    Тест загрузки и обработки excel файла
    """
    # Mocking read_excel
    mock_data = pd.DataFrame(
        {"Дата операции": ["01.01.2021 12:00:00"], "Категория": ["Продукты"], "Сумма операции": [100.50]}
    )
    mock_read_excel.return_value = mock_data

    # Преобразуем путь в строку для совместимости с вызовом read_excel
    transactions = load_transactions(str(sample_transactions_file))

    # Assertions
    assert not transactions.empty
    assert list(transactions.columns) == ["date", "category", "amount"]
    assert pd.api.types.is_datetime64_any_dtype(transactions["date"])
    assert pd.api.types.is_string_dtype(transactions["category"])
    assert pd.api.types.is_float_dtype(transactions["amount"])
    mock_read_excel.assert_called_once_with(str(sample_transactions_file))


@patch("builtins.input", side_effect=["1", "data/operations.xlsx", "каршеринг", "30.12.2020", "0"])
@patch("builtins.print")
def test_main_function(mock_print, mock_input):
    """
    Тест основной логики программы
    """
    main()

    # Проверяем, что программа вызвала input и print
    assert mock_input.call_count == 5
    mock_print.assert_any_call("Программа анализа транзакций")
    mock_print.assert_any_call("Выберите действие:")
    mock_print.assert_any_call("Результат анализа (траты по категории):")
