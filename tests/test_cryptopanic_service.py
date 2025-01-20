import pytest
from services.cryptopanic_service import CryptoPanicService
from unittest.mock import patch, Mock


@pytest.fixture
def mock_cryptopanic_response():
    # Мокируем ответ с данными от CryptoPanic API
    mock = Mock()
    mock.json.return_value = {"data": "some data from CryptoPanic"}
    return mock


def test_get_cryptopanic_data(mock_cryptopanic_response):
    service = CryptoPanicService()  # Создаем объект без передачи аргументов

    # Мокаем запрос к CryptoPanic API
    with patch('requests.get', return_value=mock_cryptopanic_response):
        response = service.make_request("https://api.cryptopanic.com")
        # Проверяем, что данные, возвращаемые сервисом, совпадают с ожидаемыми
        assert response == {"data": "some data from CryptoPanic"}
        mock_cryptopanic_response.json.assert_called_once()  # Проверяем, что метод json() был вызван один раз
