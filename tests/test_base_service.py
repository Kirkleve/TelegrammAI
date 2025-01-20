import pytest
from services.base_service import BaseService
from unittest.mock import patch, Mock


@pytest.fixture
def mock_response():
    # Настроим мок-объект с атрибутом json, который будет возвращать данные
    mock = Mock()
    mock.json.return_value = {"data": "some data"}
    return mock


def test_make_request_success(mock_response):
    service = BaseService("test")

    # Мокаем запрос
    with patch('requests.get', return_value=mock_response):
        response = service.make_request("https://api.test.com")
        # Проверяем, что данные, возвращаемые сервисом, совпадают с ожидаемыми
        assert response == {"data": "some data"}
        mock_response.json.assert_called_once()  # Проверяем, что метод json() был вызван один раз
