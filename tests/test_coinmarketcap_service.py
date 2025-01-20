import pytest
from services.coinmarketcap_service import CoinMarketCapService
from unittest.mock import patch, Mock


@pytest.fixture
def mock_coinmarketcap_response():
    # Настроим мок-объект с атрибутом json, который будет возвращать данные
    mock = Mock()
    mock.json.return_value = {"data": "some data from CoinMarketCap"}
    return mock


def test_get_coinmarketcap_data(mock_coinmarketcap_response):
    service = CoinMarketCapService()  # Создаем объект без передачи аргументов

    # Мокаем запрос к CoinMarketCap API
    with patch('requests.get', return_value=mock_coinmarketcap_response):
        response = service.make_request("https://api.coinmarketcap.com")
        # Проверяем, что данные, возвращаемые сервисом, совпадают с ожидаемыми
        assert response == {"data": "some data from CoinMarketCap"}
        mock_coinmarketcap_response.json.assert_called_once()  # Проверяем, что метод json() был вызван один раз
