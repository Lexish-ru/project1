import pytest

from src.reports import spending_by_category, spending_by_weekday, spending_by_workday


@pytest.mark.parametrize(
    "category,expected_total",
    [
        ("продукты", 1000),
        ("транспорт", 500),
        ("развлечения", 0),
    ],
)
def test_spending_by_category(sample_transactions, category, expected_total):
    result = spending_by_category(sample_transactions, category, "05.01.2021")
    if expected_total == 0:
        assert result == "Нет трат по данной категории в выбранный период."
    else:
        assert result["Общая сумма трат"].iloc[0] == expected_total


@pytest.mark.parametrize(
    "date,expected_days",
    [
        ("05.01.2021", ["Friday", "Saturday", "Sunday", "Monday", "Tuesday"]),
    ],
)
def test_spending_by_weekday(sample_transactions, date, expected_days):
    result = spending_by_weekday(sample_transactions, date)
    assert not result.empty
    assert all(day in result["day_of_week"].values for day in expected_days)


@pytest.mark.parametrize(
    "date,expected_workdays",
    [
        ("05.01.2021", {True, False}),
    ],
)
def test_spending_by_workday(sample_transactions, date, expected_workdays):
    result = spending_by_workday(sample_transactions, date)
    assert not result.empty
    assert set(result["workday"].values) == expected_workdays
