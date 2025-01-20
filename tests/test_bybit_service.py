import pytest
from services.bybit_service import BybitService
from unittest.mock import patch, Mock


@pytest.fixture
def mock_bybit_response():
    # Настроим мок-объект с атрибутом json, который будет возвращать данные
    mock = Mock()
    mock.json.return_value = {"result": "some result"}
    return mock


def test_get_bybit_data(mock_bybit_response):
    service = BybitService()  # Создаем объект без передачи аргументов

    # Мокаем запрос к Bybit API
    with patch('requests.get', return_value=mock_bybit_response):
        response = service.make_request("https://api.bybit.com")
        # Проверяем, что данные, возвращаемые сервисом, совпадают с ожидаемыми
        assert response == {"result": "some result"}
        mock_bybit_response.json.assert_called_once()  # Проверяем, что метод json() был вызван один раз
