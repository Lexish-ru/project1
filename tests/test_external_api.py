from unittest.mock import MagicMock, patch

from src.external_api import convert_to_rub


def test_convert_to_rub_usd_to_rub():
    with patch("src.external_api.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": 75.0}
        mock_get.return_value = mock_response

        result = convert_to_rub(1, "USD")
        assert result == 75.0
