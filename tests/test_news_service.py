import pytest
from services.news_service import NewsService
from unittest.mock import patch, Mock


@pytest.fixture
def mock_news_response():
    # Мокируем ответ с данными от News API
    mock = Mock()
    mock.json.return_value = {"data": "some news data"}
    return mock


def test_get_news_data(mock_news_response):
    service = NewsService()  # Создаем объект без передачи аргументов

    # Мокаем запрос к News API
    with patch('requests.get', return_value=mock_news_response):
        response = service.make_request("https://newsapi.org/v2/everything")
        # Проверяем, что данные, возвращаемые сервисом, совпадают с ожидаемыми
        assert response == {"data": "some news data"}
        mock_news_response.json.assert_called_once()  # Проверяем, что метод json() был вызван один раз
