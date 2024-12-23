import json
from pathlib import Path
from typing import Any, Dict, List


def read_transactions(json_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл с транзакциями и возвращает список словарей.
    Возвращает пустой список, если файл пустой, содержит некорректные данные или не найден.
    """
    try:
        file = Path(json_path)
        if not file.is_file():
            return []
        with open(file, encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                return []
            return data
    except (json.JSONDecodeError, FileNotFoundError, TypeError):
        return []
