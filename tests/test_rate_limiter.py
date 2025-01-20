import pytest
from rate_limiter import can_run, set_delay
from datetime import datetime, timedelta


# Мокируем хранилище задержек
@pytest.fixture
def mock_delays(monkeypatch):
    # Создаем локальное хранилище задержек
    delays = {}
    monkeypatch.setattr('rate_limiter.delays', delays)
    return delays


def test_can_run(mock_delays):
    # Установим задержку на 60 минут для функции "test_key"
    set_delay("test_key", 60)

    # Проверим, что функция не может быть выполнена сразу
    assert not can_run("test_key")

    # Изменим задержку на 0 минут и проверим, что функция может быть выполнена
    mock_delays["test_key"] = datetime.now() - timedelta(minutes=1)
    assert can_run("test_key")


def test_set_delay(mock_delays):
    # Установим задержку на 30 минут для функции "test_key"
    set_delay("test_key", 30)

    # Проверим, что задержка установлена верно
    assert "test_key" in mock_delays
    assert mock_delays["test_key"] <= datetime.now() + timedelta(minutes=30)
