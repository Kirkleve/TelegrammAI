import schedule
import time
from db_manager import create_db
from scheduler import job

# Создаём базу данных
create_db()

# Настраиваем регулярный сбор данных
schedule.every(1).minutes.do(job)

print("Сбор данных запущен...")
while True:
    schedule.run_pending()
    time.sleep(1)
