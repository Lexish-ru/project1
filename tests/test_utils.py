import json
import os
from src.utils import save_to_file

@save_to_file("test_output.json")
def sample_function():
    """Пример функции для тестирования декоратора."""
    return {"key": "value"}

def test_save_to_file():
    """Тест декоратора 'save_to_file'."""
    sample_function()
    assert os.path.exists("test_output.json")
    with open("test_output.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data == {"key": "value"}
    os.remove("test_output.json")
