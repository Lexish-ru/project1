import os

import pytest

from src.reports import spending_by_category, spending_by_weekday, spending_by_workday


def test_spending_by_category(sample_transactions):
    """Тест функции spending_by_category."""
    output_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../output")
    os.makedirs(output_dir, exist_ok=True)
    result = spending_by_category(sample_transactions, "каршеринг", "30.12.2021")
    assert result["category"] == "каршеринг"
    assert result["total_spent"] == pytest.approx(-260.53, 0.01)  # Сумма -7.07 + -257.89 + -1.32
    assert result["start_date"] == "01.10.2021"
    assert result["end_date"] == "30.12.2021"


def test_spending_by_category_no_data(sample_transactions):
    """Тест функции spending_by_category, если данных нет."""
    output_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../output")
    os.makedirs(output_dir, exist_ok=True)
    result = spending_by_category(sample_transactions, "путешествия", "30.12.2021")
    assert result["category"] == "путешествия"
    assert result["total_spent"] == 0.0


def test_spending_by_weekday(sample_transactions):
    """Тест функции spending_by_weekday."""
    output_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../output")
    os.makedirs(output_dir, exist_ok=True)
    result = spending_by_weekday(sample_transactions, "30.12.2021")
    assert result["start_date"] == "01.10.2021"
    assert result["end_date"] == "30.12.2021"
    weekdays = result["average_spending_by_weekday"]
    assert weekdays["Monday"] == pytest.approx(-67.10, 0.01)
    assert weekdays["Sunday"] == pytest.approx(-1.32, 0.01)


def test_spending_by_workday(sample_transactions):
    """Тест функции spending_by_workday."""
    output_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../output")
    os.makedirs(output_dir, exist_ok=True)
    result = spending_by_workday(sample_transactions, "30.12.2021")
    assert result["start_date"] == "01.10.2021"
    assert result["end_date"] == "30.12.2021"
    assert result["average_spending"]["workday"] == pytest.approx(-178.33, 0.01)  # Среднее по рабочим дням
    assert result["average_spending"]["weekend"] == pytest.approx(-1.32, 0.01)  # Среднее по выходным
