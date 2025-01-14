from unittest.mock import patch

import pandas as pd
import pytest

from src.reports import spending_by_category, spending_by_weekday, spending_by_workday


@pytest.mark.parametrize(
    "category, date, expected_total",
    [
        ("каршеринг", "30.12.2021", -264.96),
        ("супермаркеты", "30.12.2021", -160.89),
        ("дом и ремонт", "28.12.2021", -210.00),
        ("путешествия", "30.12.2021", 0.00),
    ],
)
def test_spending_by_category_param(
    sample_transactions: pd.DataFrame, category: str, date: str, expected_total: float
) -> None:
    """Параметризованный тест функции spending_by_category."""
    with patch("src.reports.logging") as mock_logging:
        result = spending_by_category(sample_transactions, category, date)
        assert result["category"] == category
        assert result["total_spent"] == pytest.approx(expected_total, rel=0.01)
        mock_logging.info.assert_called()


def test_spending_by_category_logic(sample_transactions: pd.DataFrame) -> None:
    """Тест логики функции spending_by_category."""
    with patch("src.reports.logging") as mock_logging:
        result = spending_by_category(sample_transactions, "каршеринг", "30.12.2021")
        assert result["category"] == "каршеринг"
        assert result["total_spent"] == pytest.approx(-264.96, rel=0.01)
        mock_logging.info.assert_called()


def test_spending_by_weekday(sample_transactions: pd.DataFrame) -> None:
    """Тест функции spending_by_weekday."""
    with patch("src.reports.logging") as mock_logging:
        result = spending_by_weekday(sample_transactions, "30.12.2021")
        weekdays = result["average_spending_by_weekday"]
        assert weekdays.get("Thursday", 0) == pytest.approx(-83.98, rel=0.01)
        assert weekdays.get("Wednesday", 0) == pytest.approx(-257.89, rel=0.01)
        mock_logging.info.assert_called()


def test_spending_by_workday(sample_transactions: pd.DataFrame) -> None:
    """Тест функции spending_by_workday."""
    with patch("src.reports.logging") as mock_logging:
        result = spending_by_workday(sample_transactions, "30.12.2021")
        assert result["average_spending"]["workday"] == pytest.approx(-158.96, 0.01)
        assert result["average_spending"]["weekend"] == pytest.approx(0.00, 0.01)
        mock_logging.info.assert_called()
