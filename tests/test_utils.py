import json
import os
from unittest.mock import mock_open, patch

from src.utils import save_to_file


@patch("os.makedirs")
@patch("builtins.open", new_callable=mock_open)
def test_save_to_file_json(mock_open_instance, mock_makedirs, sample_dataframe, sample_output_dir):
    # Относительный путь, передаваемый в декоратор
    relative_output_path = "output/test_output.json"

    # Абсолютный путь, используемый декоратором
    absolute_output_path = os.path.join(sample_output_dir, "test_output.json")

    @save_to_file(filename=relative_output_path)
    def test_function():
        return sample_dataframe

    test_function()

    # Проверяем, что os.makedirs вызван с ожидаемым абсолютным путем
    mock_makedirs.assert_called_once_with(os.path.dirname(absolute_output_path), exist_ok=True)

    # Проверяем, что open был вызван с правильным абсолютным путем
    mock_open_instance.assert_called()  # Проверяем, что `open` был вызван
    call_args = mock_open_instance.call_args  # Получаем аргументы вызова
    assert call_args[0][0] == absolute_output_path  # Проверяем путь
    assert call_args[0][1] == "w"  # Проверяем режим записи
    assert call_args[1].get("encoding") == "utf-8"  # Проверяем кодировку

    # Проверяем содержимое записанного файла
    handle = mock_open_instance()
    saved_data = json.loads(handle.write.call_args[0][0])  # Читаем данные, переданные в write
    assert len(saved_data) == len(sample_dataframe)
    assert all("column1" in row for row in saved_data)
    assert all("column2" in row for row in saved_data)
