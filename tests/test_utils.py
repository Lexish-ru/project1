import json
import os
from src.utils import save_to_file

@save_to_file("test_output.json")
def sample_function():
    """Пример функции для тестирования декоратора."""
    return {"key": "value"}

def test_save_to_file():
    """Тест декоратора 'save_to_file'."""
    # Путь к папке output
    output_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../output")
    os.makedirs(output_dir, exist_ok=True)

    # Проверяем работу декоратора
    sample_function()
    output_file = os.path.join(output_dir, "test_output.json")
    assert os.path.exists(output_file), "Файл test_output.json не был создан."

    # Проверяем содержимое файла
    with open(output_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data == {"key": "value"}, "Содержимое файла не соответствует ожидаемому."

    # Удаляем файл после теста
    os.remove(output_file)
    if not os.listdir(output_dir):  # Если папка пуста, удаляем её
        os.rmdir(output_dir)
