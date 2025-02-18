import os

import pandas as pd
import pytest


@pytest.fixture
def sample_transactions():
    data = {
        "date": pd.to_datetime(["2021-01-01", "2021-01-02", "2021-01-03", "2021-01-04", "2021-01-05"]),
        "category": ["продукты", "транспорт", "транспорт", "продукты", "продукты"],
        "amount": [100, 200, 300, 400, 500],
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_transactions_file(tmp_path):
    # Создаем временный файл для тестов
    file = tmp_path / "transactions.xlsx"
    file.write_text("test")  # Содержимое файла не имеет значения для моков
    return file


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({"column1": [1, 2, 3], "column2": ["a", "b", "c"]})


@pytest.fixture
def project_root():
    # Корень проекта - на уровень выше папки tests
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))


@pytest.fixture
def sample_output_dir(project_root):
    # Папка output внутри корня проекта
    output_dir = os.path.join(project_root, "output")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir
