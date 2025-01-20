import pytest
from services.coingecko_service import CoinGeckoService
from unittest.mock import patch, Mock


@pytest.fixture
def mock_coingecko_response():
    # Мокируем ответ с данными от CoinGecko API
    mock = Mock()
    mock.json.return_value = {"data": "some data from CoinGecko"}
    return mock


def test_get_coingecko_data(mock_coingecko_response):
    service = CoinGeckoService()  # Создаем объект без передачи аргументов

    # Мокаем запрос к CoinGecko API
    with patch('requests.get', return_value=mock_coingecko_response):
        response = service.make_request("https://api.coingecko.com")
        # Проверяем, что данные, возвращаемые сервисом, совпадают с ожидаемыми
        assert response == {"data": "some data from CoinGecko"}
        mock_coingecko_response.json.assert_called_once()  # Проверяем, что метод json() был вызван один раз
