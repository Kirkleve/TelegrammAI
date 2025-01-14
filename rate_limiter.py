from datetime import datetime, timedelta

# Хранилище задержек для функций
delays = {}

# Проверка, можно ли запускать функцию
def can_run(key):
    return key not in delays or delays[key] <= datetime.now()

# Установка задержки
def set_delay(key, delay_minutes=20):
    delays[key] = datetime.now() + timedelta(minutes=delay_minutes)
