import os
import unittest
from unittest.mock import patch

from main import main

os.chdir("/home/alexey/PycharmProjects/project1/")


class TestMainLogic(unittest.TestCase):

    @patch(
        "builtins.input",
        side_effect=["1", "data/operations.json", "EXECUTED", "да", "по убыванию", "нет", "да", "открытие"],
    )
    @patch("builtins.print")
    def test_main_json(self, mock_print, mock_input):
        """Тест логики при обработке JSON файла и правильных вводных данных"""
        main(test_mode=True, max_iterations=1)
        mock_print.assert_any_call("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
        mock_print.assert_any_call('Операции отфильтрованы по статусу "EXECUTED".')

    @patch(
        "builtins.input", side_effect=["1", "data/operations.json", "EXECUTED", "да", "по возрастанию", "нет", "нет"]
    )
    @patch("builtins.print")
    def test_main_sort_ascending(self, mock_print, mock_input):
        """Тест функции сортировки по возрастанию"""
        main(test_mode=True, max_iterations=1)
        mock_print.assert_any_call("\nОтсортировать операции по дате? Да/Нет")
        mock_print.assert_any_call(
            "Отсортировать по возрастанию или по убыванию? (введите: по возрастанию/по убыванию)"
        )

    @patch("builtins.input", side_effect=["1", "data/operations.json", "EXECUTED", "нет", "да", "да", "открытие"])
    @patch("builtins.print")
    def test_main_filter_by_description(self, mock_print, mock_input):
        """Тест работы функции поиска по ключевому слову в описании"""
        main(test_mode=True, max_iterations=1)
        mock_print.assert_any_call("\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет")
        mock_print.assert_any_call("03.02.2018 Открытие вклада")

    @patch("builtins.input", side_effect=["4", "нет"])
    @patch("builtins.print")
    def test_invalid_menu_choice(self, mock_print, mock_input):
        """Обработка некорректного ввода"""
        main(test_mode=True, max_iterations=2)
        mock_print.assert_any_call("Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    unittest.main()
