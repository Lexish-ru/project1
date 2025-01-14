import pandas as pd
import pytest


@pytest.fixture
def sample_transactions() -> pd.DataFrame:
    """Фикстура для создания тестового DataFrame с транзакциями."""
    data = {
        "date": ["2021-12-30", "2021-12-30", "2021-12-29", "2021-12-28"],
        "category": ["каршеринг", "супермаркеты", "каршеринг", "дом и ремонт"],
        "amount": [-7.07, -160.89, -257.89, -210.00],
    }
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
    return df
